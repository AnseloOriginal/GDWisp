const downloadFile = (data) => {
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'gdevelop-metadata.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  console.log("Download triggered successfully!");
}

const vecToArray = (vec) => {
  const size = vec.size()
  const ret = []
  for (let i = 0; i < size; i++) {
    ret.push(vec.get(i))
  }
  return ret;
}

const extractParameters = (instr) => {
  const size = instr.getParametersCount();
  const parametersArray = []
  for( let i = 0; i < size; i++) {
    const parameter = instr.getParameter(i)
    parametersArray.push({
      index: i,
      // ptr: parameter.ptr,
      type: parameter.getType(),
      name: parameter.getName(),
      isBehavior: parameter.isBehavior(),
      isCodeOnly: parameter.isCodeOnly(),
      isExpression: parameter.isExpression(),
      isObject: parameter.isObject(),
      // default: parameter.getDefaultValue(),
      // description: parameter.getDescription()
    })
  }
  return parametersArray
}

const extractInstructions = (instrs,object=false) => {
  const instrsList = object || {}
  const keys = vecToArray(instrs.keys());
  keys.forEach(key => {
    const instr = instrs.get(key)
    instrsList[key] = {
      // description: instr.getDescription(),
      sentence: instr.getSentence?.(), //Expression does not have sentences
      parameters: extractParameters(instr)
    }
  })
  return instrsList
}

const platform = gd.JsPlatform.get()
const exts = platform.getAllPlatformExtensions();

const mainData = {}
for (let i = 0; i < exts.size(); i++) {

  const ext = exts.get(i);

  globalActions = {}
  globalConditions = {}
  globalExpressions = {}
  const behaviourTypes = ext.getBehaviorsTypes().toJSArray()
  behaviourTypes.forEach(type => {
    extractInstructions(ext.getAllActionsForBehavior(type),globalActions)
    extractInstructions(ext.getAllConditionsForBehavior(type),globalConditions)
    extractInstructions(ext.getAllExpressionsForBehavior(type),globalExpressions)
  })
  extractInstructions(ext.getAllActionsForObject(),globalActions)
  extractInstructions(ext.getAllConditionsForObject(),globalConditions)
  extractInstructions(ext.getAllExpressionsForObject(),globalExpressions)
  const data = {
    name: ext.getName?.(),
    fullName: ext.getFullName?.(),
    subtitle: ext.getSubtitle?.(),
    description: ext.getDescription?.(),
    actions: extractInstructions(ext.getAllActions(),globalActions),
    conditions: extractInstructions(ext.getAllConditions(),globalConditions),
    expressions: extractInstructions(ext.getAllExpressions(),globalExpressions),
    namespace: ext.getNameSpace()
  }
  mainData[ext.getName()] = data
  // if (i===1) {
  //   const tmp = ext
  //   console.log(data)
  //   break
  // }
}
const finalJSON = JSON.stringify(mainData)
downloadFile(finalJSON)

