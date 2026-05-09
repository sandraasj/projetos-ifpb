const analisarTriangulo = require('./triangulo');

function testar(descricao, resultadoEsperado, resultadoObtido) {
  const passou = JSON.stringify(resultadoEsperado) === JSON.stringify(resultadoObtido);

  console.log(`\nTeste: ${descricao}`);
  console.log("Esperado:", resultadoEsperado);
  console.log("Obtido :", resultadoObtido);
  console.log(passou ? "✅ PASSOU" : "❌ FALHOU");
}


testar(
  "Triângulo equilátero",
  { formaTriangulo: true, tipo: "Equilátero" },
  analisarTriangulo(3, 3, 3)
);

testar(
  "Triângulo escaleno",
  { formaTriangulo: true, tipo: "Escaleno" },
  analisarTriangulo(3, 4, 5)
);

testar(
  "Triângulo isósceles",
  { formaTriangulo: true, tipo: "Isósceles" },
  analisarTriangulo(3, 3, 4)
);

testar(
  "Não forma triângulo (soma inválida)",
  { formaTriangulo: false, motivo: "A soma de dois lados não é maior que o terceiro." },
  analisarTriangulo(1, 2, 3)
);

testar(
  "Não forma triângulo (lado negativo)",
  { formaTriangulo: false, motivo: "Os lados devem ser maiores que zero." },
  analisarTriangulo(-1, 2, 3)
);