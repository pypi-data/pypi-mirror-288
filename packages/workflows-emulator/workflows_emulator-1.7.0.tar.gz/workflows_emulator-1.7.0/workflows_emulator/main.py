import copy
import json
import logging
from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, NoReturn, Optional

import yaml
from jsonschema import validate
from requests import HTTPError

from workflows_emulator.lib.http_utils import (
    AUTH_OAUTH2,
    request as authenticated_request,
)
from workflows_emulator.render import assign_var, render_config, run_code
from workflows_emulator.utils import (
    Context, DISCOVERY_DOCUMENTS_PATH, SpecialNextStep,
    NextStep, ReturnValue,
    STEP_NOT_FOUND, StepConfig,
    UnhandledBranchError, WorkflowError, load_package_config,
)

logger = logging.getLogger('workflows')

# TODO: implement SafeLineLoader to enrich the error messages
# class SafeLineLoader(SafeLoader):
#     def construct_mapping(self, node, deep=False):
#         mapping = super(SafeLineLoader, self).construct_mapping(node,
#         deep=deep)
#         # Add 1 so line numbering starts at 1
#         mapping['__line__'] = node.start_mark.line + 1
#         return mapping

def load_config(config_path: str) -> dict:
    """Load a configuration file from a given path."""
    with open(config_path) as file:
        return yaml.safe_load(file)


WORKFLOW_SCHEMA = load_package_config('workflow-schema.json')


def load_workflow(config_path: str) -> Dict:
    """Load a workflow from a given path."""
    workflow = load_config(config_path)
    validate(workflow, WORKFLOW_SCHEMA)
    return workflow


def execute_workflow(config: dict | list[dict], params: dict) -> any:
    """
    Runs a workflow given a configuration and parameters.

    We need the whole config inside the prams to run try/retry "predicate" and
    to be able to call other sub-workflows. Also, having it in the context is
    cleaner than storing it in a global variable
    """
    # if the root is a list of steps instead of a map with a 'main' key
    if isinstance(config, list):
        config = {'main': {'steps': config}}

    main_config = config.pop('main')
    logger.info(f"Running 'main' workflow: params -> {json.dumps(params)}")
    return execute_subworkflow(main_config, params, config)


def get_params(workflow_params: list[str | dict], runtime_params: dict) -> dict:
    context = {}
    for param in workflow_params:
        if isinstance(param, dict):
            param_name = list(param.keys())[0]
            param_value = param[param_name]
            context[param_name] = runtime_params.get(param_name, param_value)
        else:
            try:
                context[param] = runtime_params[param]
            except KeyError:
                raise KeyError(f"Missing workflow parameter: {param}")
    return context


def execute_subworkflow(workflow: dict, params: dict, context: dict) -> any:
    """Executes a subworkflow given a configuration and parameters.

    The context is required since it stores the rest of sub-workflows that might
    need to be called.
    """
    solved_params = get_params(workflow.get('params', []), params)
    logger.info(f"Running subworkflow")
    logger.debug(
        f"Subworkflow started: : params -> {json.dumps(solved_params)}"
    )
    context.update(solved_params)
    _ctxt, next_step, ret_value = execute_steps_list(workflow['steps'], context)
    if next_step not in [None, SpecialNextStep.END]:
        raise ValueError(f"Step {next_step} not found in the workflow")
    logger.info(f"Subworkflow complete: result -> {json.dumps(ret_value)}")
    return ret_value


class Step(ABC):

    def __init__(self, step_id: str, config: StepConfig, context: Context):
        self.step_id = step_id
        self.config = config
        self.context = context
        step_type = self.__class__.__name__.replace('Step', '').lower()
        self.logger = logging.getLogger('workflows.' + step_type)

    @abstractmethod
    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        pass


def keep_only_subworkflows(context: Context) -> Context:
    """
    Receives a Context and returns a new context with only the subworkflows
    """
    return {
        key: value
        for key, value in context.items()
        if isinstance(value, dict) and 'steps' in value
    }


class StepReturn(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        ret_value = render_config(self.config['return'], self.context)
        return self.context, None, ret_value


class StepFor(Step):

    @staticmethod
    def inclusive_range(start: int | float, end: int | float):
        """Returns a range from start to end inclusive."""
        # if start is float
        if isinstance(start, float) or isinstance(end, float):
            elements = []
            while start <= end:
                elements.append(start)
                start += 1.0
            return elements
        return range(start, end + 1)

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        config = self.config['for']
        copy_context = copy.deepcopy(self.context)
        # determine the kind of loop
        if 'in' in config:
            iterable = render_config(config['in'], copy_context)
        else:
            iterable_range = render_config(config['range'], copy_context)
            iterable = StepFor.inclusive_range(*iterable_range)
        index_variable = config.get('index', '__index')
        value_variable = config.get('value', '__value')
        next_step = None
        ret_value = None
        for index, value in enumerate(iterable):
            self.logger.debug(
                f"  Iterating: {index_variable}={index}, "
                f"{value_variable}={value}"
            )
            copy_context[index_variable] = index
            copy_context[value_variable] = value
            copy_context, next_step, ret_value = StepSteps(
                step_id=self.step_id,
                config=config,
                context=copy_context
            ).execute()
            if next_step == SpecialNextStep.BREAK:
                next_step = None
                break
            if next_step == SpecialNextStep.CONTINUE:
                next_step = None
                continue
            if next_step == SpecialNextStep.END:
                break
            if ret_value is not None or next_step is not None:
                break
        copy_context.pop(index_variable)
        copy_context.pop(value_variable)

        # update the parent context with the new variables
        offending_vars = [
            key for key in copy_context.keys()
            if key not in self.context
        ]
        if offending_vars:
            self.logger.warning(
                f'Variables {offending_vars} in `for` step "{self.step_id}" '
                f'are not parent context and will be discarded'
            )
        update_vars = {
            key: value
            for key, value in copy_context.items()
            if key in self.context and self.context[key] != value
        }
        self.context.update(update_vars)
        return self.context, next_step, ret_value


class StepRaise(Step):

    def execute(self) -> NoReturn:
        rendered_error = render_config(self.config['raise'], self.context)
        # suppose that the error is a string by default
        error_map = {
            'message': rendered_error,
            'tags': ['WorkflowException'],
        }
        # if it was a dictionary use it instead
        if isinstance(rendered_error, dict):
            error_map = rendered_error

        raise WorkflowError(
            **error_map,
        )


class StepNext(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        self.logger.debug(f"  Next step: {self.config.get('next')}")
        return self.context, self.config.get('next'), None


class StepTry(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        step = self.config
        context = self.context
        try:
            return execute_step(self.step_id, step['try'], context)
        except WorkflowError as err:
            error_var = step['except']['as']
            context[error_var] = err.map
            return execute_steps_list(step['except']['steps'], context)


class StepRetry(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        step = self.config
        context = self.context
        logger = self.logger
        retry_config = render_config(step['retry'], context)
        if 'backoff' in retry_config:
            backoff_config = retry_config['backoff']
            delay = backoff_config['initial_delay']
            max_delay = backoff_config['max_delay']
            multiplier = backoff_config['initial_delay']
        predicate = retry_config.get('predicate', None)
        raised_err = None
        for retry_num in range(retry_config['max_retries'] + 1):
            try:
                if retry_num > 0:
                    logger.debug(f"Retry -> Attempt {retry_num}")
                return execute_step(self.step_id, step['try'], context)
            except WorkflowError as err:
                raised_err = err
                # check if we need to execute the predicate
                if predicate is not None:
                    logger.info(f"Retry -> Running predicate")
                    run_result = execute_subworkflow(
                        workflow=predicate,
                        params={'e': err.map},
                        context=keep_only_subworkflows(context)
                    )
                    # if the predicate asserts it's not a retryable error break
                    if not run_result:
                        logger.error("Retry -> Error type not supported "
                                          "by "
                                 "predicate")
                        break
                # do the sleep
                if 'backoff' in retry_config:
                    logger.debug(f"Retry -> waiting {delay} seconds")
                    if delay < max_delay:
                        sleep(delay)
                        delay *= multiplier
                    # we run out of time but the issue was not fixed
                    else:
                        logger.error(f"Retry -> timeout {max_delay=}")
                        break
        # if retries run out, but not the max_delay and the predicate
        # didn't fix it
        else:
            logger.error(f"Retry -> Max retries reached")
        if 'except' in step:
            error_var = step['except']['as']
            context[error_var] = raised_err.map
            return execute_steps_list(step['except']['steps'], context)
        else:
            raise raised_err


class StepSteps(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Executes a list of steps.

        The steps are executed sequentially. If a step returns a value, the
        execution stops and the value is returned.

        All variables assigned within are accessible in the upper workflow
        context.
        """
        step_list = self.config['steps']
        context = self.context
        new_context, next_step, ret_value = execute_steps_list(
            step_list,
            context
        )
        context.update(new_context)
        return context, next_step, ret_value


def preserve_context(context: Context, new_context: Context) -> Context:
    """Preserves the context variables that are not in the new context."""
    new_vars = {
        key: new_context.get(key, value)
        for key, value in context.items()
    }
    context.update(new_vars)
    return context

class StepAssign(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Assigns a value to a variable in the context.

        Variable names are rendered before assignment. So it allows for map
        and list index assignment."""
        context = self.context
        _context = {} # only for logging purposes
        for var in self.config['assign']:
            var_name = list(var.keys())[0]
            var_value = var[var_name]
            rendered_value = render_config(var_value, context)
            root_key, new_val = assign_var(var_name, rendered_value, context)
            context[root_key] = new_val
            _context[root_key] = new_val
        self.logger.debug(json.dumps(_context))
        return context, self.config.get('next'), None


class StepCall(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Executes a call step.

        The call step can be a call to a Google API, a subworkflow, or a Python
        function from the standard library."""
        step = self.config
        context = self.context
        logger = self.logger
        rendered_step = render_config(step, context)
        callable_name = rendered_step['call']
        if callable_name.startswith('googleapis.'):
            logger.debug(f"Calling Connector: {callable_name}")
            run_result = StepCall.execute_connector(rendered_step)
        # call another subworkflow
        elif callable_name in context:
            logger.debug(f"Call Subworkflow: {callable_name}")
            run_result = execute_subworkflow(
                workflow=context[callable_name],
                params=rendered_step.get('args', {}),
                context=keep_only_subworkflows(context)
            )
        # call a python function from the standard library
        else:
            fn_args = rendered_step.get('args', {})
            log_args = ', '.join([f"{k}={v}" for k, v in fn_args.items()])
            logger.debug(f"Call std lib method: `{callable_name}({log_args})`")
            args_str = "**_args" if isinstance(fn_args, dict) else "*_args"
            run_result = run_code(
                code=f'{callable_name}({args_str})',
                context={**context, '_args': fn_args}
            )
        if 'result' in rendered_step:
            context[step['result']] = run_result

        return context, step.get('next'), None

    @staticmethod
    def execute_connector(rendered_step: StepConfig) -> Context:
        """Executes a connector step.

        The connector step is a call to a Google API. It retrieves the
        service url and http verb from the discovery documents."""

        # googleapis.service_name.version.[resource1[.resource2[...]]].method
        call_parts = rendered_step['call'].split('.')
        _, service_name, version, *resources, method = call_parts
        # @formatter:off
        service_discovery_file_path = f'{DISCOVERY_DOCUMENTS_PATH}/{service_name}_{version}.json'
        # @formatter:on
        service_discovery_config = load_package_config(
            service_discovery_file_path
        )
        # iteratively consume the parts to get the final config
        next_part = service_discovery_config
        for resource in resources:
            next_part = next_part['resources'][resource]
        final_config = next_part['methods'][method]

        # now that we have the actual method config, extract the information
        scopes = final_config['scopes']
        http_verb: str = final_config['httpMethod']
        base_url = service_discovery_config['rootUrl']
        config_path = final_config['path'].replace('+', '')
        service_path = service_discovery_config['servicePath']
        final_url_template = base_url + service_path + config_path
        # replaces the variables in the url
        final_url = run_code(
            code=f'f"""{final_url_template}"""',
            context=rendered_step['args']
        )
        # make the request
        logger.debug(f"  {http_verb.upper()} {final_url}")
        result = authenticated_request(
            url=final_url,
            auth=AUTH_OAUTH2,
            body=rendered_step['args'].get('body', None),
            method=http_verb,
            scopes=scopes
        )
        return result['body']


class StepParallel(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        try:
            return self.try_execute()
        except Exception as err:
            branch_err = UnhandledBranchError.__class__.__name__
            raise UnhandledBranchError(
                message=f"{branch_err}: One or more branches or iterations "
                        f"encountered an unhandled runtime error",
                tags=[
                    UnhandledBranchError.__class__.__name__,
                    err.__class__.__name__
                ],
                branches=[
                    {
                        'id': self.step_id,
                        'error': f"{err.__class__.__name__}: {err.args[0]}"
                    }
                ]
            )

    def try_execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Emulates running steps in parallel.

        As this is an emulator and not the actual workflow engine, steps will
        be executed sequentially.

        Only variables available in the outer context are preserved"""
        context_copy = copy.deepcopy(self.context)
        config = self.config['parallel']
        if 'for' in config:
            step_executor = StepFor(
                step_id=self.step_id,
                config=config,
                context=context_copy
            )
        # if not 'for', then it is 'branches'
        else:
            step_executor = StepSteps(
                step_id=self.step_id,
                config={'steps': config['branches']},
                context=context_copy
            )
        result_context, next_step, _ret_value = step_executor.execute()
        # get new variables from the parallel execution
        new_vars = {
            key: value
            for key, value in result_context.items()
            if key not in self.context or self.context[key] != value
        }
        # check if new assigned variables are in the shared list
        shared_vars = set(config.get('shared', []))
        set_new_vars = set(new_vars.keys())
        if not set_new_vars.issubset(shared_vars):
            offending_vars = set_new_vars - shared_vars
            raise RuntimeError(
                f'Variables {offending_vars} in parallel step "{self.step_id}" '
                f'are not in the shared variables list: {shared_vars}'
            )
        # update the context with the new variables
        if next_step is not None:
            raise RuntimeError(
                f"Cannot use `next: {next_step}` pointing outside the "
                f"parallel step"
            )
        if _ret_value is not None:
            raise RuntimeError(
                f"Cannot return a value from a parallel step"
            )
        return result_context, None, None


class StepSwitch(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Checks each condition of the switch and executes the inner step.

        Inner step is run if condition evaluates to True.
        """
        context = self.context
        for condition in self.config['switch']:
            # evaluate the condition and remove the field
            condition_copy = copy.deepcopy(condition)
            evaluated_condition = render_config(
                condition_copy['condition'],
                context
            )
            if not isinstance(evaluated_condition, bool):
                raise ValueError(
                    f'The switch condition must evaluate to a boolean: `'
                    f'{condition_copy["condition"]}`'
                )
            if evaluated_condition:
                condition_copy.pop('condition')
                context, next_step, ret_value = execute_step(
                    step_id=self.step_id,
                    config=condition_copy,
                    context=context
                )
                if ret_value is not None or next_step is not None:
                    return context, next_step, ret_value
        return context, self.config.get('next'), None


def execute_steps_list(
    steps: list[dict[str, StepConfig]],
    context: Context,
    next_step: NextStep = None,
) -> tuple[Context, Optional[NextStep], ReturnValue]:
    """
    It either returns a context and a ret_value or a step_id to go to and
    continue execution

    Returns:
    - context: The context after executing the steps
    - next_step: The step id to go to, or None to continue with the next step
    - ret_value: The return value of the steps
    """
    ret_value = None
    while True:
        step_id, step_index, step_config = get_step(steps, next_step)
        # if the next_step was SET but NOT FOUND, return to search in the parent
        if step_index == STEP_NOT_FOUND:
            break
        logger.info(f"Step running: `{step_id}`")
        context, next_step, ret_value = execute_step(
            step_id,
            step_config,
            context
        )
        if ret_value is not None:
            break
        # if the step did not return a next_step, get the next step in the list
        match next_step:
            case SpecialNextStep.END:
                # keep it's 'end' value for the outer scope
                break
            case None:
                # continue with the next step in the list
                if step_index + 1 < len(steps):
                    next_step = list(steps[step_index + 1].keys())[0]
                    continue
                else:
                    break
            case _:
                # allow to search for the next_step in the next iteration
                continue
        # if the list returned a next_step, will be used in the next iteration
    return context, next_step, ret_value


def execute_step(
    step_id: NextStep,
    config: StepConfig,
    context: Context
) -> tuple[Context, Optional[NextStep], ReturnValue]:
    """Executes the step and returns the context and, if any, the result and
    return value

    Returns:
    - context: The context after executing the step
    - next: None to go to the next step, or the step id to go to a specific step
    - return: The return value of the step
    """
    logger.debug(f"  Step type: {'/'.join(config.keys())}")
    try:
        StepExecutor = get_step_executor(config)
        step_instance = StepExecutor(
            step_id=step_id,
            config=config,
            context=context
        )
        return step_instance.execute()
    except WorkflowError as err:
        raise err
    except (
        ConnectionError, TypeError, ValueError, KeyError,
        SystemError, TimeoutError, IndexError, RecursionError, ZeroDivisionError
    ) as err:
        raise WorkflowError(
            message=err.args[0],
            tags=[err.__class__.__name__],
        )
    except HTTPError as err:
        body = err.response.text
        if 'application/json' in err.response.headers.get('Content-Type', ''):
            body = err.response.json()
        raise WorkflowError(
            message=err.args[0],
            tags=[err.__class__.__name__],
            code=err.response.status_code,
            headers=dict(err.response.headers),
            body=body,
        )


def get_step(
    steps: list[dict], step_id: str
) -> tuple[str | None, int, dict]:
    """Returns the index of the step with the given id, or -1 if not found."""
    if step_id is None:
        step_id = list(steps[0].keys())[0]
        return step_id, 0, steps[0][step_id]
    for index, step in enumerate(steps):
        if list(step.keys())[0] == step_id:
            return step_id, index, step[step_id]
    return None, STEP_NOT_FOUND, {}


def get_step_executor(step_config: StepConfig) -> type[Step]:
    """Step factory method.

    Determines the executor to use given a step config. The lookup is
    prioritized since —for example— `retry` and `try` behave different. Or in a
    step having `assign` and `next`we would like to run `assign` first and let
    it handle the `next` field.
    """
    step_type_lookup = [
        ('call', StepCall),
        ('return', StepReturn),
        ('assign', StepAssign),
        ('raise', StepRaise),
        ('retry', StepRetry),
        ('try', StepTry),
        ('steps', StepSteps),
        ('for', StepFor),
        ('parallel', StepParallel),
        ('switch', StepSwitch),
        ('next', StepNext),
    ]
    for step_field, step_executor in step_type_lookup:
        if step_field in step_config:
            return step_executor
    raise RuntimeError(f"Step type not found in {step_config.keys()}")
