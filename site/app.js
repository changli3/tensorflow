const express = require('express')
const app = express()
const port = 9999
const { exec } = require('child_process');

app.use (function(req, res, next) {
  var data='';
  req.setEncoding('binary');
  req.on('data', function(chunk) {
    data += chunk;
  });

  req.on('end', function() {
    req.body = data;
    next();
  });
});

app.get('/', (request, response) => {
  response.send('The node connector is running!')
})

app.post('/predict', (req, response) => {
  var cmd = './run-predict "' + req.body + '"';
  exec(cmd, (err, stdout, stderr) => {
  if (err) {
		response.send('womething wrong - ' + err);
        return;
  }
	response.send(`${stderr}  ${stdout}`);
  });
})

app.listen(port, (err) => {
  if (err) {
    return console.log('Error -', err)
  }
  console.log(`server is listening on ${port}`)
})