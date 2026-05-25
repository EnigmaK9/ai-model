// Flowchart.js diagram definition using state-based syntax for color coding
// You can test and render this code at http://flowchart.js.org/

var code = `
st=>start: Start: Uvicorn Server|past
opLifespan=>operation: lifespan Context Manager|past
condStartup=>condition: Model loaded successfully?|past
opLoad=>operation: Load Tokenizer & Model into memory|past
opYield=>operation: Print Success & Yield Control (App Ready)|past
opFailMsg=>operation: Print Error & Raise Exception|invalid
eFail=>end: Server Fails to Start|invalid

subShutdown=>subroutine: Trigger: On Shutdown|invalid
opUnload=>operation: Unload model & tokenizer resources|invalid
opClearCache=>operation: Clear cache (torch.cuda.empty_cache)|invalid
eStop=>end: Server Stopped|invalid

opReceive=>operation: Receive POST /chat (AgentRequest)|current
condEmpty=>condition: Prompt empty?|approved
sub400=>subroutine: 400 Bad Request|rejected
condLoaded=>condition: Model initialized?|approved
sub503=>subroutine: 503 Service Unavailable|rejected

opPipeline=>operation: Define messages (System + User)|future
opTemplate=>operation: Apply chat template (apply_chat_template)|future
opEncode=>operation: Encode input to PyTorch tensors|future
opInference=>operation: Local generation (model.generate with torch.no_grad)|future
opDecode=>operation: Decode output tokens to text|future

condException=>condition: Exception caught?|approved
sub500=>subroutine: 500 Internal Server Error|rejected
op200=>operation: 200 OK: Return AgentResponse|future

st->opLifespan->condStartup
condStartup(yes)->opLoad->opYield
condStartup(no)->opFailMsg->eFail

subShutdown->opUnload->opClearCache->eStop

opYield->opReceive->condEmpty
condEmpty(yes)->sub400
condEmpty(no)->condLoaded

condLoaded(no)->sub503
condLoaded(yes)->opPipeline->opTemplate->opEncode->opInference->opDecode->condException

condException(yes)->sub500
condException(no)->op200
`;

// Configuration options mapping the state keywords to specific colors
var options = {
  'symbols': {},
  'styles': {
    'past': {
      'fill': '#e1f5fe',
      'stroke': '#0288d1',
      'stroke-width': 2
    },
    'current': {
      'fill': '#fff3e0',
      'stroke': '#f57c00',
      'stroke-width': 2
    },
    'approved': {
      'fill': '#ede7f6',
      'stroke': '#5e35b1',
      'stroke-width': 2
    },
    'future': {
      'fill': '#e8f5e9',
      'stroke': '#388e3c',
      'stroke-width': 2
    },
    'rejected': {
      'fill': '#ffebee',
      'stroke': '#c62828',
      'stroke-width': 2
    },
    'invalid': {
      'fill': '#eceff1',
      'stroke': '#455a64',
      'stroke-width': 2
    }
  }
};

var chart = flowchart.parse(code);
chart.drawSVG('canvas', options);