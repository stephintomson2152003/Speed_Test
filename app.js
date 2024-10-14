// app.js
const express = require('express');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/process', (req, res) => {
  const inputData = req.body.data;

  exec(`python scripts/data_processor.py "${inputData}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send('Error processing data');
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`);
      return res.status(500).send('Error in Python script');
    }

    const result = JSON.parse(stdout);
    res.json(result);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
