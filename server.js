const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 9876;
const WINDOW_SIZE = 10;

let numbers = [];

app.get('/numbers/:type', async (req, res) => {
  const type = req.params.type;
  let url = '';
  try {
    switch(type) {
      case 'p': url = 'http://20.244.56.144/test/primes'; break;
      case 'f': url = 'http://20.244.56.144/test/fibo'; break;
      case 'e': url = 'http://20.244.56.144/test/even'; break;
      case 'r': url = 'http://20.244.56.144/test/rand'; break;
      default: return res.status(400).json({ error: 'Invalid type' });
    }

    const response = await axios.get(url);
    const newNumbers = response.data.numbers;
    numbers = [...new Set([...numbers, ...newNumbers])].slice(-WINDOW_SIZE);

    const avg = numbers.reduce((a, b) => a + b, 0) / numbers.length;

    res.json({
      windowPrevState: numbers.slice(0, -1),
      windowCurrState: numbers,
      numbers: newNumbers,
      avg: avg.toFixed(2)
    });
  } catch (error) {
    res.status(500).json({ error: 'Error fetching numbers' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
