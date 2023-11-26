const express = require('express');
const router = express.Router();
const connection = require('../connection');

// Rota para exibir a página com o gráfico
router.get('/', (req, res) => {
  connection.query('SELECT S.cpf, S.nome AS NomeServidor, S.cargo, U.nome AS NomeUniversidade, I.nome AS NomeInstituto FROM Servidor S JOIN Instituto I ON S.fk_Instituto_nome = I.nome AND S.fk_Universidade_id_uni = I.fk_Universidade_id_uni LEFT JOIN Universidade U ON S.fk_Universidade_id_uni = U.id_uni;', (error, results) => {
    if (error) throw error;

    res.render('info', { results: results });
  });
});

router.get('/media', (req, res) => {
  connection.query(`SELECT
  U.nome AS NomeUniversidade,
  S.cargo ,
  AVG(R.bruto) AS MediaSalario
FROM
  Universidade U
JOIN
  Instituto I ON U.id_uni = I.fk_Universidade_id_uni
JOIN
  Servidor S ON I.nome = S.fk_Instituto_nome AND I.fk_Universidade_id_uni = S.fk_Universidade_id_uni
JOIN
  Remuneracao R ON S.id_servidor = R.fk_Servidor_id_servidor
GROUP BY
  U.nome, S.cargo;
`, (error, results) => {
    if (error) throw error;

    res.render('media', { results: results });
  });
});

module.exports = router;
