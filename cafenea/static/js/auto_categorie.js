
window.addEventListener('load', function () {
    const denumireField = document.querySelector('#id_denumire');
    const categorieField = document.querySelector('#id_categorie');

    if (categorieField) {
        categorieField.readOnly = true;
        categorieField.style.cursor = "not-allowed";
        categorieField.style.pointerEvents = "none";
    }

    // const mapare = {
    //     'Espresso': 'Cafele', 
    //     'Espresso Lung': 'Cafele',
    //     'Espresso Decaf': 'Cafele',
    //     'Espresso Machiatto': 'Cafele',
    //     'Espresso Con Panna': 'Cafele', 
    //     'Americano': 'Cafele',
    //     'Flat White': 'Cafele', 
    //     'Cappuccino': 'Cafele',
    //     'Ciocolata calda': 'Bauturi Calde', 
    //     'Ceai': 'Bauturi Calde',
    //     'Coca-Cola': 'Soft Drinks', 'Pepsi': 'Soft Drinks',
    //     'Negresa': 'Dulciuri', 'Briosa': 'Dulciuri'
    // };

    const structuraCategorii = {
        'Cafele': [
            'Espresso', 'Espresso Lung', 'Espresso Decaf', 'Espresso Machiatto', 
            'Espresso Con Panna', 'Americano', 'Cappuccino', 'Caffe Latte', 'Flat White',
        ],
        'Bauturi Calde': [
            'Ciocolata Calda', 'Chai Latte', 'Ceai',
        ],
        'Bauturi Reci': [
            'Iced Coffee', 'Greek Frappe', 'Ness Frappe', 'Espresso Tonic', 'Milkshake', 'Smoothie',
        ],
        'Soft Drinks': [
            'Coca-Cola', 'Fanta', 'Sprite', 'Pepsi', 'Apa Plata', 'Apa Minerala', 'RedBull',
        ],
        'Dulciuri': [
            'Negresa', 'Fursec American', 'Briosa', 'Biscuite cu ovaz', 'Mini Croissant', 'Biscuiti Vegani', 'Salam de Biscuiti', 'Ciocolata de Casa',
        ]
    };

    const mapare_finala = {};

    for (const [categorie, produse] of Object.entries(structuraCategorii)) {
        produse.forEach(produs => {
            mapare_finala[produs] = categorie;
        });
    }

    if (denumireField && categorieField) {
        denumireField.addEventListener('change', function () {
            const produsSelectat = this.value;
            categorieField.value = mapare_finala[produsSelectat] || "";
            if (mapare[produsSelectat]) {
                categorieField.value = mapare[produsSelectat];
            }
        });
    }
});