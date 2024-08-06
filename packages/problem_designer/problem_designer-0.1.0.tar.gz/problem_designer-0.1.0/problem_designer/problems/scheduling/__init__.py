from problem_designer.problems.scheduling.flow_shop.generator import (
    FlowShopGenerator,
    FlowShopGeneratorOptions,
)
from problem_designer.problems.scheduling.flow_shop.spec import (
    FlowShopDesignSpec,
    FlowShopMeta,
)
from problem_designer.problems.scheduling.job_shop.generator import (
    JobShopGenerator,
    JobShopGeneratorOptions,
)
from problem_designer.problems.scheduling.job_shop.spec import (
    JobShopDesignSpec,
    JobShopMeta,
)
from problem_designer.problems.scheduling.open_shop.generator import (
    OpenShopGenerator,
    OpenShopGeneratorOptions,
)
from problem_designer.problems.scheduling.open_shop.spec import (
    OpenShopDesignSpec,
    OpenShopMeta,
)
from problem_designer.typedef.plugin import (
    DesignHookConstants,
    DesignSpecPlugin,
    GeneratorHookConstants,
    GeneratorPlugin,
)


@DesignHookConstants.impl
def register_spec():
    return [
        DesignSpecPlugin(OpenShopMeta(), OpenShopDesignSpec),
        DesignSpecPlugin(FlowShopMeta(), FlowShopDesignSpec),
        DesignSpecPlugin(JobShopMeta(), JobShopDesignSpec),
    ]


@GeneratorHookConstants.impl
def register_generator():
    return [
        GeneratorPlugin(OpenShopMeta(), OpenShopGenerator, OpenShopGeneratorOptions),
        GeneratorPlugin(FlowShopMeta(), FlowShopGenerator, FlowShopGeneratorOptions),
        GeneratorPlugin(JobShopMeta(), JobShopGenerator, JobShopGeneratorOptions),
    ]
