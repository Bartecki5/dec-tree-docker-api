async function wyslijDoAPI() {
    
    const danePacjenta = {
        Age: parseInt(document.getElementById('age').value),
        Sex: document.getElementById('sex').value,
        ChestPainType: document.getElementById('chestpain').value,
        RestingBP: parseInt(document.getElementById('restingbp').value),
        Cholesterol: parseInt(document.getElementById('cholesterol').value),
        FastingBS: parseInt(document.getElementById('fastingbs').value),
        RestingECG: document.getElementById('restingecg').value,
        MaxHR: parseInt(document.getElementById('maxhr').value),
        ExerciseAngina: document.getElementById('exangina').value,
        Oldpeak: parseFloat(document.getElementById('oldpeak').value),
        ST_Slope: document.getElementById('stslope').value
    };

    try {
        const odpowiedz = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(danePacjenta)
        });

        const daneZSerwera = await odpowiedz.json();
        const poleWyniku = document.getElementById('wynik');
        poleWyniku.style.display = "block";
        
        if (daneZSerwera.Diagnoza === 1) {
            poleWyniku.style.backgroundColor = "#ffe6e6";
            poleWyniku.style.color = "#cc0000";
            poleWyniku.innerText = "🚨 " + daneZSerwera.Komunikat;
        } else {
            poleWyniku.style.backgroundColor = "#e6ffe6";
            poleWyniku.style.color = "#006600";
            poleWyniku.innerText = "✅ " + daneZSerwera.Komunikat;
        }
    } catch (error) {
        alert("Błąd połączenia z serwerem. Czy uvicorn jest włączony w terminalu?");
    }
}
