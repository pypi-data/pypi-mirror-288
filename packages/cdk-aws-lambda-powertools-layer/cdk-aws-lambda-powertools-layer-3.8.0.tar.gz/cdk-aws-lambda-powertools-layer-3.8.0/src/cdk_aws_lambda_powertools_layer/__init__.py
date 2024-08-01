r'''
# Powertools for AWS Lambda Layer

## Why this project exists

This is a custom construct that will create AWS Lambda Layer with Powertools for AWS Lambda for Python or NodeJS library. There are different
ways how to create a layer and when working with CDK you need to install the library, create a zip file and wire it
correctly. With this construct you don't have to care about packaging and dependency management. Create a construct
and add it to your function. The construct is an extension of the
existing [`LayerVersion`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.LayerVersion.html) construct
from the CDK library, so you have access to all fields and methods.

> ⚠️ **This construct uses docker to build and bundle the dependencies!**

See the [API](API.md) for details.

```python
import {LambdaPowertoolsLayer} from 'cdk-aws-lambda-powertools-layer';
import {RuntimeFamily } from "aws-cdk-lib/aws-lambda";

  const powertoolsLayerPython = new LambdaPowertoolsLayer(this, 'TestLayer', {runtimeFamily: RuntimeFamily.PYTHON});
  const powertoolsLayerNodeJS = new LambdaPowertoolsLayer(this, 'TestLayer', {runtimeFamily: RuntimeFamily.NODEJS});
```

Python

```python
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer

powertoolsLayer = LambdaPowertoolsLayer(self, 'PowertoolsLayer')
```

The layer will be created during the CDK `synth` step and thus requires Docker.

## Install

TypeSript/JavaScript:

```shell
npm i cdk-aws-lambda-powertools-layer
```

Python:

```shell
pip install cdk-aws-lambda-powertools-layer
```

## Usage

### Python

A single line will create a layer with Powertools for AWS Lambda (Python). For NodeJS you need to specifically set the `runtimeFamily: Runtime.NODEJS` property.

```python
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer

powertoolsLayer = LambdaPowertoolsLayer(self, 'PowertoolsLayer')
```

You can then add the layer to your funciton:

```python
from aws_cdk import aws_lambda

aws_lambda.Function(self, 'LambdaFunction',
                            code=aws_lambda.Code.from_asset('function'),
                            handler='app.handler',
                            layers=[powertoolsLayer])
```

You can specify the powertools version by passing the optional `version` paramter, otherwise the construct will take the
latest version from pypi repository.

```python
LambdaPowertoolsLayer(self, 'PowertoolsLayer', version='1.24.0')
```

Additionally, powertools have extras depenedncies such as
Pydantic, [documented here](https://awslabs.github.io/aws-lambda-powertools-python/latest/#lambda-layer). This is not
included by default, and you have to set this option in the construct definition if you need it:

```python
LambdaPowertoolsLayer(self, 'PowertoolsLayer', include_extras=True)
```

Full example:

```python
from aws_cdk import Stack, aws_lambda
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer
from constructs import Construct


class LayerTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertoolsLayer = LambdaPowertoolsLayer(
            self, 'PowertoolsLayer', include_extras=True, version='1.24.0')

        aws_lambda.Function(self, 'LambdaFunction',
                            code=aws_lambda.Code.from_asset('function'),
                            handler='app.handler',
                            layers=[powertoolsLayer])

```

### TypeScript

Full example for TypeScript:

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LambdaPowertoolsLayer } from 'cdk-aws-lambda-powertools-layer';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

export class CdkPowertoolsExampleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const powertoolsLayer = new LambdaPowertoolsLayer(this, 'TestLayer', {
      version: '1.22.0',
      includeExtras: true
    });

    new Function(this, 'LambdaFunction', {
      code: Code.fromAsset(path.join('./function')),
      handler: 'app.handler',
      layers: [powertoolsLayer],
    });
  }
}
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class LambdaPowertoolsLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-lambda-powertools-layer.LambdaPowertoolsLayer",
):
    '''Defines a new Lambda Layer with Powertools for AWS Lambda (Python) library.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''creates build argument for the Dockerfile.

        There are multiple combinations between version and extras package that results in different suffix for the installation.
        With and without version, with and without extras flag.
        We construct one suffix here because it is easier to do in code than inside the Dockerfile with bash commands.
        For example, if we set ``includeExtras=true`` and ``version=1.22.0`` we get '[all]==1.22.0'.

        :param scope: -
        :param id: -
        :param compatible_architectures: The compatible architectures for the layer.
        :param include_extras: A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The Powertools for AWS Lambda package version from pypi repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52989f8cfc13e7d6247276ec304b50ed3fbc22151b0a48e8e5aa9349cf367ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PowertoolsLayerProps(
            compatible_architectures=compatible_architectures,
            include_extras=include_extras,
            layer_version_name=layer_version_name,
            runtime_family=runtime_family,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class LambdaPowertoolsLayerPythonV3(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-lambda-powertools-layer.LambdaPowertoolsLayerPythonV3",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        python_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
        compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CDK Layer for Python v3 *.

        :param scope: -
        :param id: -
        :param python_version: The Python version for Powertools for AWS Lambda (Python) V3. Allowed values: Runtime.PYTHON_3_8 Runtime.PYTHON_3_9 Runtime.PYTHON_3_10 Runtime.PYTHON_3_11 Runtime.PYTHON_3_12
        :param compatible_architectures: The compatible architectures for the layer.
        :param include_extras: A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The Powertools for AWS Lambda package version from pypi repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b493af5e63bdb3f890ae79064f0566d01bcfb34c50a8d9157a44e374a2f552d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PowertoolsPythonLayerProps(
            python_version=python_version,
            compatible_architectures=compatible_architectures,
            include_extras=include_extras,
            layer_version_name=layer_version_name,
            runtime_family=runtime_family,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-aws-lambda-powertools-layer.PowertoolsLayerProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_architectures": "compatibleArchitectures",
        "include_extras": "includeExtras",
        "layer_version_name": "layerVersionName",
        "runtime_family": "runtimeFamily",
        "version": "version",
    },
)
class PowertoolsLayerProps:
    def __init__(
        self,
        *,
        compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for Powertools for AWS Lambda (Python) Layer.

        :param compatible_architectures: The compatible architectures for the layer.
        :param include_extras: A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The Powertools for AWS Lambda package version from pypi repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccfc4c316e2527e42747269f47e940b83a85392bfaf4b6b9b041944ee2fcf4c)
            check_type(argname="argument compatible_architectures", value=compatible_architectures, expected_type=type_hints["compatible_architectures"])
            check_type(argname="argument include_extras", value=include_extras, expected_type=type_hints["include_extras"])
            check_type(argname="argument layer_version_name", value=layer_version_name, expected_type=type_hints["layer_version_name"])
            check_type(argname="argument runtime_family", value=runtime_family, expected_type=type_hints["runtime_family"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_architectures is not None:
            self._values["compatible_architectures"] = compatible_architectures
        if include_extras is not None:
            self._values["include_extras"] = include_extras
        if layer_version_name is not None:
            self._values["layer_version_name"] = layer_version_name
        if runtime_family is not None:
            self._values["runtime_family"] = runtime_family
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def compatible_architectures(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.Architecture]]:
        '''The compatible architectures for the layer.'''
        result = self._values.get("compatible_architectures")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.Architecture]], result)

    @builtins.property
    def include_extras(self) -> typing.Optional[builtins.bool]:
        '''A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.'''
        result = self._values.get("include_extras")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def layer_version_name(self) -> typing.Optional[builtins.str]:
        '''the name of the layer, will be randomised if empty.'''
        result = self._values.get("layer_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_family(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily]:
        '''the runtime of the layer.'''
        result = self._values.get("runtime_family")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Powertools for AWS Lambda package version from pypi repository.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PowertoolsLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-lambda-powertools-layer.PowertoolsPythonLayerProps",
    jsii_struct_bases=[PowertoolsLayerProps],
    name_mapping={
        "compatible_architectures": "compatibleArchitectures",
        "include_extras": "includeExtras",
        "layer_version_name": "layerVersionName",
        "runtime_family": "runtimeFamily",
        "version": "version",
        "python_version": "pythonVersion",
    },
)
class PowertoolsPythonLayerProps(PowertoolsLayerProps):
    def __init__(
        self,
        *,
        compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
        python_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    ) -> None:
        '''Defines a new Lambda Layer with Powertools for AWS Lambda (Python) library.

        :param compatible_architectures: The compatible architectures for the layer.
        :param include_extras: A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The Powertools for AWS Lambda package version from pypi repository.
        :param python_version: The Python version for Powertools for AWS Lambda (Python) V3. Allowed values: Runtime.PYTHON_3_8 Runtime.PYTHON_3_9 Runtime.PYTHON_3_10 Runtime.PYTHON_3_11 Runtime.PYTHON_3_12
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e82d3d6d57bc27e6dd15124dec601cfc1a2f89a73ff68a37dd710b0a7941917)
            check_type(argname="argument compatible_architectures", value=compatible_architectures, expected_type=type_hints["compatible_architectures"])
            check_type(argname="argument include_extras", value=include_extras, expected_type=type_hints["include_extras"])
            check_type(argname="argument layer_version_name", value=layer_version_name, expected_type=type_hints["layer_version_name"])
            check_type(argname="argument runtime_family", value=runtime_family, expected_type=type_hints["runtime_family"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compatible_architectures is not None:
            self._values["compatible_architectures"] = compatible_architectures
        if include_extras is not None:
            self._values["include_extras"] = include_extras
        if layer_version_name is not None:
            self._values["layer_version_name"] = layer_version_name
        if runtime_family is not None:
            self._values["runtime_family"] = runtime_family
        if version is not None:
            self._values["version"] = version
        if python_version is not None:
            self._values["python_version"] = python_version

    @builtins.property
    def compatible_architectures(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.Architecture]]:
        '''The compatible architectures for the layer.'''
        result = self._values.get("compatible_architectures")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.Architecture]], result)

    @builtins.property
    def include_extras(self) -> typing.Optional[builtins.bool]:
        '''A flag for the extras dependencies (pydantic, aws-xray-sdk, etc.) This will increase the size of the layer significantly. If you don't use parsing, ignore it.'''
        result = self._values.get("include_extras")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def layer_version_name(self) -> typing.Optional[builtins.str]:
        '''the name of the layer, will be randomised if empty.'''
        result = self._values.get("layer_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_family(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily]:
        '''the runtime of the layer.'''
        result = self._values.get("runtime_family")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Powertools for AWS Lambda package version from pypi repository.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_version(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime]:
        '''The Python version for Powertools for AWS Lambda (Python) V3.

        Allowed values:
        Runtime.PYTHON_3_8
        Runtime.PYTHON_3_9
        Runtime.PYTHON_3_10
        Runtime.PYTHON_3_11
        Runtime.PYTHON_3_12
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PowertoolsPythonLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaPowertoolsLayer",
    "LambdaPowertoolsLayerPythonV3",
    "PowertoolsLayerProps",
    "PowertoolsPythonLayerProps",
]

publication.publish()

def _typecheckingstub__d52989f8cfc13e7d6247276ec304b50ed3fbc22151b0a48e8e5aa9349cf367ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
    include_extras: typing.Optional[builtins.bool] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b493af5e63bdb3f890ae79064f0566d01bcfb34c50a8d9157a44e374a2f552d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    python_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
    include_extras: typing.Optional[builtins.bool] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccfc4c316e2527e42747269f47e940b83a85392bfaf4b6b9b041944ee2fcf4c(
    *,
    compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
    include_extras: typing.Optional[builtins.bool] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e82d3d6d57bc27e6dd15124dec601cfc1a2f89a73ff68a37dd710b0a7941917(
    *,
    compatible_architectures: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.Architecture]] = None,
    include_extras: typing.Optional[builtins.bool] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    runtime_family: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeFamily] = None,
    version: typing.Optional[builtins.str] = None,
    python_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass
