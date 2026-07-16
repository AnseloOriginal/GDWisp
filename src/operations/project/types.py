from __future__ import annotations
from typing import TypedDict, NotRequired, Union, Required, Any, Literal

class ProjectData(TypedDict):
	firstLayout: str
	gdVersion: GdVersionData
	properties: ProjectPropertiesData
	resources: ResourcesData
	usedResources: list[ResourceReference]
	objects: list[ObjectData]
	variables: list[RootVariableData]
	layouts: list[LayoutData]
	externalLayouts: list[ExternalLayoutData]
	eventsFunctionsExtensions: list[EventsFunctionsExtensionData]
	activatedByDefaultInEditorBehaviors: NotRequired[list[str]]

class EventsFunctionsVariablesData(TypedDict):
	name: str
	variables: list[RootVariableData]

class ObjectData(TypedDict):
	name: str
	type: str
	variables: list[RootVariableData]
	behaviors: list[BehaviorData | dict[str, Any]]
	effects: list[EffectData]
	usedResources: NotRequired[list[ResourceReference]]

class ResourceReference(TypedDict):
	name: str

class EffectData(TypedDict):
	effectType: str
	name: str
	disabled: NotRequired[bool]
	doubleParameters: dict[str, float]
	stringParameters: dict[str, str]
	booleanParameters: dict[str, bool]


class BehaviorData(TypedDict):
	name: str
	type: str


class ObjectGroupData(TypedDict):
	name: str
	objects: list[ObjectGroupDataObjectsType]

type VariableType = Literal["string", "number", "boolean", "structure", "array"]

class VariableData(TypedDict):
	name: NotRequired[str]
	value: NotRequired[str | float | bool]
	children: NotRequired[list[VariableData]]
	type: VariableType

class RootVariableData(VariableData):
	name: Required[str]


class ProjectPropertiesData(TypedDict):
	adaptGameResolutionAtRuntime: str
	folderProject: bool
	orientation: str
	packageName: str
	projectFile: str
	scaleMode: Literal["linear", "nearest"]
	pixelsRounding: bool
	antialiasingMode: Literal["none", "MSAA"]
	antialisingEnabledOnMobile: bool
	sizeOnStartupMode: Literal[ "" , "scaleOuter" , "adaptWidth" , "adaptHeight"]
	version: str
	name: str
	author: str
	authorIds: list[str]
	authorUsernames: list[str]
	windowWidth: int
	windowHeight: int
	latestCompilationDirectory: str
	maxFPS: int
	minFPS: int
	verticalSync: bool
	loadingScreen: LoadingScreenData
	watermark: WatermarkData
	currentPlatform: str
	extensionProperties: list[ExtensionProperties]
	useDeprecatedZeroAsDefaultZOrder: NotRequired[bool]
	useDeprecatedZeroAsDefaultStringVariable: NotRequired[bool]
	projectUuid: NotRequired[str]
	sceneResourcePreloading: Literal["at-startup", "never"]
	sceneResourcesUnloading: Literal["at-scene-exit", "never"]
	areEffectsHiddenInEditor: NotRequired[bool]

class ExtensionProperties(TypedDict):
	extension: str
	property: str
	value: str


class WatermarkData(TypedDict):
	showWatermark: bool
	placement: Literal["top-left", "top-right", "bottom-left", "bottom-right", "bottom", "top"]


class LoadingScreenData(TypedDict):
	showGdevelopSplash: bool
	backgroundImageResourceName: str
	backgroundColor: int
	backgroundFadeInDuration: float
	minDuration: float
	logoAndProgressFadeInDuration: float
	logoAndProgressFadeInDelay: float
	showProgressBar: bool
	progressBarMinWidth: float
	progressBarMaxWidth: float
	progressBarWidthPercent: float
	progressBarHeight: float
	progressBarColor: int

class ObjectGroupDataObjectsType(TypedDict):
	name: str 

class GdVersionData(TypedDict):
	build: int
	major: int
	minor: int
	revision: int

class ResourcesReference(TypedDict):
	resources: list[ResourcesData]

class ResourceData(TypedDict):
	file: str
	kind: ResourceKind
	metadata: str
	name: str
	smoothed: NotRequired[bool]
	userAdded: bool
	disablePreload: bool
	preloadAsSound: bool
	preloadAsMusic: bool
	preloadInCache: bool

class InstanceContainerData(TypedDict):
	variables: list[RootVariableData]
	instances: list[InstanceData]
	objects: list[ObjectData]
	objectGroups: list[ObjectGroupData]
	layers: list[LayerData]

class LayoutData(InstanceContainerData):
	r: int
	v: int
	b: int
	mangledName: str
	name: str
	stopSoundsOnStartup: bool
	title: str
	behaviorSharedData: list[behaviorSharedData]
	usedResources: list[ResourceReference]
	resourcePreloading: NotRequired[Literal['at-startup', "never", "inherit"]]
	resourceUnloading: NotRequired[Literal["at-scene-exit", "never", "inherit"]]
	uiSettings: InstancesEditorSettings
	events: list[EventData]

class behaviorSharedData(TypedDict): 
	name: str
	type: str

class LayerData(TypedDict):
	name: str
	renderingType: NotRequired[Literal["", "2d", "3d", "2d+3d"]]
	cameraType: NotRequired[Literal["perspective","orthographic"]]
	defaultCameraBehavior: NotRequired[Literal["top-left-anchored-if-never-moved", "do-nothing"]]
	visibility: bool
	cameras: list[CameraData]
	effects: list[EffectData]
	_hiddenEffects: NotRequired[list[EffectData]]
	ambientLightColorR: int
	ambientLightColorG: int
	ambientLightColorB: int
	camera3DFieldOfView: NotRequired[float]
	camera3DFarPlaneDistance: NotRequired[float]
	camera3DNearPlaneDistance: NotRequired[float]
	camera2DPlaneMaxDrawingDistance: NotRequired[float]
	isLightingLayer: bool
	followBaseLayerCamera: bool
	isLocked: NotRequired[bool]

class InstancesEditorSettings(TypedDict):
	grid: bool
	gridType: Literal["rectangular", "isometric"]
	gridWidth: float
	gridHeight: float
	gridDepth: NotRequired[float]
	gridOffsetX: float
	gridOffsetY: float
	gridOffsetZ: NotRequired[float]
	gridColor: int
	gridAlpha: float
	snap: bool

class CameraData(TypedDict):
	defaultSize: bool
	defaultViewport: bool
	height: int
	viewportBottom: int
	viewportLeft: int
	viewportRight: int
	viewportTop: int
	width: int

class InstancePersistentUuidData(TypedDict):
	persistentUuid: str

class InstanceData(InstancePersistentUuidData):
	layer: str
	locked: NotRequired[bool]
	sealed: NotRequired[bool]
	name: str
	x: int
	y: int
	z: NotRequired[float]
	angle: int
	rotationX: int
	rotationY: int
	zOrder: int
	opacity: NotRequired[float]
	flippedX: bool
	flippedY: bool
	flippedZ: bool
	customSize: bool
	width: int
	height: int
	depth: int
	numberProperties: list[InstanceNumberProperty]
	stringProperties: list[InstanceStringProperty]
	initialVariables: list[RootVariableData]
	behaviorsOverridings: NotRequired[ObjectGroupDataObjectsType | dict[str, Any]]

class ExternalLayoutData(TypedDict):
	name: str
	associatedLayout: str
	instances: list[InstanceData]
	editorSettings: InstancesEditorSettings

class EventsFunctionsExtensionData(TypedDict):
	name: str
	eventsBasedObjects: list[EventsBasedObjectData]
	globalVariables: list[RootVariableData]
	sceneVariables: list[RootVariableData]

class EventsBasedObjectVariantData(InstanceContainerData):
	name: str
	areaMinX: float
	areaMinY: float
	areaMinZ: float
	areaMaxX: float
	areaMaxY: float
	areaMaxZ: float
	_initialInnerArea: EventsBasedObjectVariantDataInitialInnerArea | None
	instances: list[InstanceData]
	layers: list[LayerData]
	usedResources: list[ResourceReference]
	editorSettings: InstancesEditorSettings

class EventsBasedObjectVariantDataInitialInnerArea(TypedDict):
	min: tuple[float, float, float]
	max: tuple[float, float, float]

class EventsBasedObjectData(EventsBasedObjectVariantData):
	name: str
	isInnerAreaFollowingParentSize: bool
	variants: list[EventsBasedObjectVariantData]
	defaultVariant: NotRequired[EventsFunctionsVariablesData]

class ResourcesData(TypedDict):
  resources: list[ResourceData]

type ResourceKind = Literal['audio', 'image', 'font', 'video', 'json', 'tilemap',
'tileset', 'bitmapFont', 'model3D', 'atlas', 'spine', 'internal-in-game-editor-only-svg',
'fake-resource-kind-for-testing-only']

class InstanceNumberProperty(TypedDict):
  name: str
  value: int

class InstanceStringProperty(TypedDict):
  name: str
  value: str

class JsCodeEventData(TypedDict):
	type: Literal["BuiltinCommonInstructions::JsCode"]
	inlineCode: str | list[str]
	parameterObjects: str
	useStrict: bool
	eventsSheetExpanded: bool
	disabled: NotRequired[bool]
	folded: NotRequired[bool]

class InstructionData(TypedDict):
    type: dict[str, str]
    parameters: list[str]
    subInstructions: NotRequired[list[InstructionData]]

class CommentEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Comment"]
    color: CommentEventColorData
    comment: str
    comment2: NotRequired[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class CommentEventColorData(TypedDict):
    r: int
    g: int
    b: int
    textR: int
    textG: int
    textB: int

class ElseEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Else"]
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class ForEachChildVariableEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::ForEachChildVariable"]
    iterableVariableName: str
    valueIteratorVariableName: str
    keyIteratorVariableName: str
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    loopIndexVariable: NotRequired[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class ForEachEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::ForEach"]
    object: str
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    loopIndexVariable: NotRequired[str]
    orderBy: NotRequired[str]
    order: NotRequired[str]
    limit: NotRequired[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class GroupEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Group"]
    name: str
    source: str
    creationTime: int
    colorR: int
    colorG: int
    colorB: int
    events: list[EventData]
    parameters: list[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class LinkEventIncludeData(TypedDict):
    includeConfig: int
    eventsGroup: NotRequired[str]
    start: NotRequired[int]
    end: NotRequired[int]

class LinkEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Link"]
    include: LinkEventIncludeData
    target: str
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class RepeatEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Repeat"]
    repeatExpression: str
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    loopIndexVariable: NotRequired[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class StandardEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::Standard"]
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

class WhileEventData(TypedDict):
    type: Literal["BuiltinCommonInstructions::While"]
    infiniteLoopWarning: bool
    whileConditions: list[InstructionData]
    conditions: list[InstructionData]
    actions: list[InstructionData]
    events: NotRequired[list[EventData]]
    variables: NotRequired[list[RootVariableData]]
    loopIndexVariable: NotRequired[str]
    disabled: NotRequired[bool]
    folded: NotRequired[bool]

type EventData = Union[
    StandardEventData,
    ElseEventData,
    RepeatEventData,
    WhileEventData,
    ForEachEventData,
    ForEachChildVariableEventData,
    CommentEventData,
    GroupEventData,
    LinkEventData,
    JsCodeEventData
]
