const express = require('express');
const router = express.Router();
const connection = require('../connection');

// Rota para exibir a página com o gráfico
router.get('/', (req, res) => {
  connection.query('SELECT * FROM servidores', (error, results) => {
    if (error) throw error;

    res.render('index', { results: results });
  });
});

router.get('/servidores', (req, res) => {
  res.render('servidores', { teste: "teste" });
});

module.exports = router;
