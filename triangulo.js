function analisarTriangulo(a, b, c) {

  if (a <= 0 || b <= 0 || c <= 0) {
    return {
      formaTriangulo: false,
      motivo: "Os lados devem ser maiores que zero."
    };
  }

  if (a + b <= c || a + c <= b || b + c <= a) {
    return {
      formaTriangulo: false,
      motivo: "A soma de dois lados não é maior que o terceiro."
    };
  }

  let tipo = "";

  if (a === b && b === c) {
    tipo = "Equilátero";
  } else if (a === b || a === c || b === c) {
    tipo = "Isósceles";
  } else {
    tipo = "Escaleno";
  }

  return {
    formaTriangulo: true,
    tipo: tipo
  };
}

module.exports = analisarTriangulo;