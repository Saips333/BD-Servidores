const express = require('express');
const router = express.Router();
const connection = require('../connection');

// Rota para exibir a página com o gráfico
router.get('/', (req, res) => {
  connection.query('SELECT S.id_servidor, S.cpf, S.nome AS NomeServidor, S.cargo, U.nome_uni AS NomeUniversidade, I.nome_instituto AS NomeInstituto FROM Servidor S JOIN Instituto I ON S.fk_servidor_instituto = I.id_instituto AND S.fk_servidor_universidade = I.fk_instituto_universidade LEFT JOIN Universidade U ON S.fk_servidor_universidade = U.id_uni;', (error, results) => {
    if (error) throw error;

    res.render('info', { results: results });
  });
});

router.get('/media', (req, res) => {
  connection.query(`
  SELECT
  U.nome_uni AS NomeUniversidade,
  S.cargo ,
  AVG(R.val_bruto) AS MediaSalario
  FROM
    Universidade U
  JOIN
    Instituto I ON U.id_uni = I.fk_instituto_universidade
  JOIN
    Servidor S ON I.id_instituto = S.fk_servidor_instituto AND I.fk_instituto_universidade = S.fk_servidor_universidade
  JOIN
    Remuneracao R ON S.id_servidor = R.fk_remuneracao_servidor
  GROUP BY
    U.nome_uni, S.cargo;
`, (error, results) => {
    if (error) throw error;

    res.render('media', { results: results });
  });
});

router.get('/remuneracao', (req, res) => {
  connection.query(`
  SELECT 
    S.cpf, 
    S.nome AS NomeServidor, 
    R.val_bruto, 
    R.outras_deducoes, 
    R.val_ferias, 
    R.val_natal 
  FROM 
    Servidor S 
  LEFT JOIN 
    Remuneracao R ON S.id_servidor = R.fk_remuneracao_servidor;`, (error, results) => {
      if (error) throw error;

      res.render('remuneracao', { results: results });
  });
});

router.get('/deducoes', (req, res) => {
  connection.query(`
  SELECT
    U.nome_uni AS NomeUniversidade,
    I.nome_instituto AS NomeInstituto,
    SUM(R.outras_deducoes) AS TotalDeducoes
  FROM
      Universidade U
  JOIN
      Instituto I ON U.id_uni = I.fk_instituto_universidade
  JOIN
      Servidor S ON I.id_instituto = S.fk_servidor_instituto AND I.fk_instituto_universidade = S.fk_servidor_universidade
  JOIN
      Remuneracao R ON S.id_servidor = R.fk_remuneracao_servidor
  GROUP BY
      U.nome_uni, I.nome_instituto
  HAVING
      TotalDeducoes < 0;
  `, (error, results) => {
    if (error) throw error;

    res.render('deducoes', { results: results });
  });
});
router.get('/acima', (req, res) => {
  connection.query(`
  WITH AvgSalaries AS (
    SELECT 
        S.fk_servidor_universidade, 
        AVG(R.val_bruto) AS AvgSalary
    FROM 
        Remuneracao R
    JOIN 
        Servidor S ON R.fk_remuneracao_servidor = S.id_servidor
    GROUP BY 
        S.fk_servidor_universidade
  )
  SELECT
    S.cpf,
    S.nome AS NomeServidor,
    S.cargo,
    U.nome_uni AS NomeUniversidade,
    I.nome_instituto AS NomeInstituto,
    R.val_bruto AS Salario
  FROM
    Servidor S
  JOIN
    Remuneracao R ON S.id_servidor = R.fk_remuneracao_servidor
  JOIN
    Universidade U ON S.fk_servidor_universidade = U.id_uni
  JOIN
    Instituto I ON S.fk_servidor_instituto = I.id_instituto AND S.fk_servidor_universidade = I.fk_instituto_universidade
  JOIN
    AvgSalaries A ON S.fk_servidor_universidade = A.fk_servidor_universidade
  WHERE
    R.val_bruto > A.AvgSalary;
  `, (error, results) => {
    if (error) throw error;

    res.render('acima', { results: results });
  });
});
module.exports = router;