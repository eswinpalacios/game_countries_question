// Variables globales
let countries = [];
let currentCountry = null;
let score = 0;
let currentQuestion = 0;
const TOTAL_QUESTIONS = 4;

// Elementos del DOM
const startScreen = document.getElementById('start-screen');
const gameScreen = document.getElementById('game-screen');
const resultScreen = document.getElementById('result-screen');
const startBtn = document.getElementById('start-btn');
const nextBtn = document.getElementById('next-btn');
const restartBtn = document.getElementById('restart-btn');
const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options');
const feedbackElement = document.getElementById('feedback');
const scoreElement = document.getElementById('score');
const finalScoreElement = document.getElementById('final-score');
const flagContainer = document.getElementById('flag-container');
const flagImage = document.getElementById('flag');

// Tipos de preguntas
const QUESTION_TYPES = [
    {
        type: 'capital',
        getQuestion: (country) => `¿Cuál es la capital de ${country.name}?`,
        getAnswer: (country) => country.capital
    },
    {
        type: 'currency',
        getQuestion: (country) => `¿Cuál es la moneda de ${country.name}?`,
        getAnswer: (country) => country.currency
    },
    {
        type: 'language',
        getQuestion: (country) => `¿Cuál es el idioma oficial de ${country.name}?`,
        getAnswer: (country) => country.language
    },
    {
        type: 'region',
        getQuestion: (country) => `¿En qué región se encuentra ${country.name}?`,
        getAnswer: (country) => country.region
    },
    {
        type: 'subregion',
        getQuestion: (country) => `¿En qué subregión se encuentra ${country.name}?`,
        getAnswer: (country) => country.subregion
    },
    {
        type: 'flag',
        getQuestion: () => '¿A qué país pertenece esta bandera?',
        getAnswer: (country) => country.name
    }
];

// Cargar datos de países
async function loadCountries() {
    try {
        const response = await fetch('source/countries.json');
        countries = await response.json();
        console.log('Países cargados:', countries.length);
    } catch (error) {
        console.error('Error al cargar los países:', error);
        alert('Error al cargar los datos del juego. Por favor, recarga la página.');
    }
}

// Iniciar el juego
function startGame() {
    score = 0;
    currentQuestion = 0;
    scoreElement.textContent = score;
    startScreen.classList.add('hidden');
    gameScreen.classList.remove('hidden');
    nextQuestion();
}

// Generar una nueva pregunta
function nextQuestion() {
    if (currentQuestion >= TOTAL_QUESTIONS) {
        endGame();
        return;
    }

    // Reiniciar estado
    nextBtn.classList.add('hidden');
    feedbackElement.textContent = '';
    optionsContainer.innerHTML = '';
    flagContainer.classList.add('hidden');

    // Seleccionar un país aleatorio
    currentCountry = countries[Math.floor(Math.random() * countries.length)];
    
    // Seleccionar un tipo de pregunta aleatorio
    const questionType = QUESTION_TYPES[Math.floor(Math.random() * QUESTION_TYPES.length)];
    
    // Configurar la pregunta
    questionText.textContent = questionType.getQuestion(currentCountry);
    
    // Mostrar la bandera si es una pregunta de bandera
    if (questionType.type === 'flag') {
        flagImage.src = currentCountry.flag;
        flagImage.alt = `Bandera de ${currentCountry.name}`;
        flagContainer.classList.remove('hidden');
    }
    
    // Obtener la respuesta correcta
    const correctAnswer = questionType.getAnswer(currentCountry);
    
    // Generar opciones de respuesta
    const options = [correctAnswer];
    
    // Añadir opciones incorrectas
    while (options.length < 4) {
        let randomCountry;
        let answer;
        
        // Asegurarse de que las opciones incorrectas sean únicas
        do {
            randomCountry = countries[Math.floor(Math.random() * countries.length)];
            answer = questionType.getAnswer(randomCountry);
        } while (options.includes(answer));
        
        options.push(answer);
    }
    
    // Mezclar las opciones
    shuffleArray(options);
    
    // Crear botones de opciones
    options.forEach(option => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = option;
        button.onclick = () => selectAnswer(option, correctAnswer);
        optionsContainer.appendChild(button);
    });
    
    currentQuestion++;
}

// Manejar la selección de respuesta
function selectAnswer(selectedAnswer, correctAnswer) {
    const buttons = document.querySelectorAll('.option-btn');
    let isCorrect = selectedAnswer === correctAnswer;
    
    // Deshabilitar todos los botones
    buttons.forEach(button => {
        button.disabled = true;
        
        // Resaltar la respuesta correcta
        if (button.textContent === correctAnswer) {
            button.classList.add('correct');
        }
        
        // Resaltar la respuesta incorrecta si se seleccionó una
        if (button.textContent === selectedAnswer && !isCorrect) {
            button.classList.add('incorrect');
        }
    });
    
    // Actualizar puntuación y mostrar retroalimentación
    if (isCorrect) {
        score++;
        scoreElement.textContent = score;
        feedbackElement.textContent = '¡Correcto! ¡Buen trabajo!';
        feedbackElement.style.color = '#155724';
    } else {
        feedbackElement.textContent = `Incorrecto. La respuesta correcta es: ${correctAnswer}`;
        feedbackElement.style.color = '#721c24';
    }
    
    nextBtn.classList.remove('hidden');
}

// Finalizar el juego
function endGame() {
    gameScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    finalScoreElement.textContent = `${score} de ${TOTAL_QUESTIONS}`;
}

// Reiniciar el juego
function restartGame() {
    resultScreen.classList.add('hidden');
    startGame();
}

// Función auxiliar para mezclar un array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Cargar los países al iniciar
    loadCountries();
    
    // Configurar botones
    startBtn.addEventListener('click', startGame);
    nextBtn.addEventListener('click', nextQuestion);
    restartBtn.addEventListener('click', restartGame);
});
