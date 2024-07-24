const canvas = document.querySelector('canvas');
const form = document.querySelector('.signature-pad-form');
const clearButton = document.querySelector('.clear-button');
const signatureInput = document.getElementById('signature-input');

const ctx = canvas.getContext('2d');
let writingMode = false;

// Function to get the position (X, Y) based on event type (touch or mouse)
const getTargetPosition = (event) => {
    let positionX, positionY;
    if (event.type.startsWith('touch')) {
        // For touch events
        positionX = event.touches[0].clientX - event.target.getBoundingClientRect().x;
        positionY = event.touches[0].clientY - event.target.getBoundingClientRect().y;
    } else {
        // For mouse events
        positionX = event.clientX - event.target.getBoundingClientRect().x;
        positionY = event.clientY - event.target.getBoundingClientRect().y;
    }
    return [positionX, positionY];
};

const handlePointerMove = (event) => {
    if (!writingMode) return;
    const [positionX, positionY] = getTargetPosition(event);
    ctx.lineTo(positionX, positionY);
    ctx.stroke();
};

const handlePointerUp = () => {
    writingMode = false;
};

const handlePointerDown = (event) => {
    writingMode = true;
    ctx.beginPath();
    const [positionX, positionY] = getTargetPosition(event);
    ctx.moveTo(positionX, positionY);
};

// Event listeners for both touch and mouse events
canvas.addEventListener('pointerdown', handlePointerDown, {passive: true});
canvas.addEventListener('pointerup', handlePointerUp, {passive: true});
canvas.addEventListener('pointermove', handlePointerMove, {passive: true});

// Clear the canvas
const clearPad = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

clearButton.addEventListener('click', (event) => {
    event.preventDefault();
    clearPad();
});

// Submit the signature (you can modify this part as needed)
form.addEventListener('submit', (event) => {
    event.preventDefault();
    const imageURL = canvas.toDataURL();
    signatureInput.value = imageURL;
    form.submit();
    // Display the image (optional)
    const image = document.createElement('img');
    image.src = imageURL;
    image.height = canvas.height;
    image.width = canvas.width;
    image.style.display = 'block';
    form.appendChild(image);
    clearPad();
});
