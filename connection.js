const mysql = require('mysql');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'servidores',
  //port: 33061,
});

connection.connect((err) => {
  if (err) {
    console.error('Erro na conexão com o banco de dados: ' + err.message);
  } else {
    console.log('Conectado ao banco de dados');
  }
});

module.exports = connection;
