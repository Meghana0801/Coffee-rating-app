async function loadCoffees() {

    const response = await fetch('/coffees');
    const coffees = await response.json();

    const coffeeList = document.getElementById('coffeeList');

    coffeeList.innerHTML = '';

    coffees.forEach(coffee => {

        coffeeList.innerHTML += `
            <div class="coffee-card">
                <h2>${coffee.name}</h2>
                <p>Votes: ${coffee.votes}</p>

                <button onclick="voteCoffee(${coffee.id})">
                    Vote
                </button>
            </div>
        `;
    });
}

async function voteCoffee(id) {

    await fetch(`/vote/${id}`, {
        method: 'POST'
    });

    loadCoffees();
}

loadCoffees();