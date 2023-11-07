const express = require('express');
const router = express.Router();
const connection = require('../connection');

// Rota para exibir a página com o gráfico
router.get('/', (req, res) => {
  connection.query('SELECT * FROM professors', (error, results) => {
    if (error) throw error;

    res.render('index', { professores: results });
  });
});

module.exports = router;
