const root = document.documentElement;
const weight = document.getElementById('weight');
const size = document.getElementById('size');
const reading = document.getElementById('reading');

const update = () => {
    root.style.setProperty('--weight', weight.value);
    root.style.setProperty('--size', `${size.value}px`);
    document.getElementById('weight-out').textContent = weight.value;
    document.getElementById('size-out').textContent = size.value;
    document.body.classList.toggle('reading-forms', reading.checked);
};

const weights = document.getElementById('weights');
for (const value of [200, 300, 400, 500, 600, 700]) {
    const line = document.createElement('p');
    line.style.fontWeight = String(value);
    const label = document.createElement('span');
    label.textContent = String(value);
    line.append(label, document.createTextNode('Exportar mapa de Guadalajara'));
    weights.append(line);
}

weight.addEventListener('input', update);
size.addEventListener('input', update);
reading.addEventListener('change', update);
update();
