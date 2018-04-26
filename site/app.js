const express = require('express')
var uuid = require('node-uuid');
const app = express()
const port = 9999
const { exec } = require('child_process');
var fileUpload = require('express-fileupload');

app.use(express.static('mesStatic'));
app.use(fileUpload());

app.post('/mnist-predict', (req, response) => {
  var image = req.files.file;
  var fileName = uuid.v1();
  image.mv(__dirname + '/uploads/' + fileName, function(err) {
     if(err){
       console.log(err);
       response.send(err);
     }else{
       console.log("uploaded");
       var cmd = './run-mnist-predict "' + fileName  + '"';
       exec(cmd, (err, stdout, stderr) => {
         if (err) {
          response.send('something wrong - ' + err);
         } else
          response.send(`${stderr}  ${stdout}`);
       });
     }
  });
})


app.post('/predict', (req, response) => {
  var image = req.files.file;
  var fileName = uuid.v1();
  image.mv(__dirname + '/uploads/' + fileName, function(err) {
     if(err){
       console.log(err);
       response.send(err);
     }else{
       console.log("uploaded");
       var cmd = './run-predict "' + fileName  + '"';
       exec(cmd, (err, stdout, stderr) => {
         if (err) {
          response.send('something wrong - ' + err);
         } else
          response.send(`${stderr}  ${stdout}`);
       });
     }
  });
})

app.listen(port, (err) => {
  if (err) {
    return console.log('Error -', err)
  }
  console.log(`server is listening on ${port}`)
})
        