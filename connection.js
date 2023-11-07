const mysql = require('mysql');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'professores',
});

connection.connect((err) => {
  if (err) {
    console.error('Erro na conexão com o banco de dados: ' + err.message);
  } else {
    console.log('Conectado ao banco de dados');
  }
});

module.exports = connection;
