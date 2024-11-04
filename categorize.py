import pandas as pd
import re

# Define main categories with their respective subcategories and keywords in Hungarian
categories = {
    "Pizzafajták": {
        "Margarita": ["margarita", "margherita"],
        "Prosciutto": ["prosciutto", "sonka", "serrano", "parma ham", "parmezán"],
        "Funghi": ["funghi", "gomba", "mushroom", "erdei gombás"],
        "Hawaii": ["hawaii", "ananász", "sonka", "pineapple"],
        "Gyros": ["gyros", "tzatziki", "görög", "greek"],
        "Vegetáriánus": ["vegetáriánus", "zöldséges", "zöldség", "vegetable", "veggie", "verdure"],
        "Pepperoni": ["pepperoni", "szalámi", "salami"],
        "BBQ": ["bbq", "barbecue", "barbeque", "grillezett"],
        "Kebabos": ["kebab", "doner", "saslik", "shawarma", "kebabos"],
        "Tenger gyümölcsei": ["tenger gyümölcsei", "rák", "kagyló", "polip", "seafood", "frutti di mare"],
        "Tonhal": ["tonhal", "hal", "tuna", "füstölt hal"],
        "Sajtos": ["sajtos", "3 kívánság", "5 kívánság", "cheese", "mozzarella", "four cheese", "négysajtos"],
        "Special": ["firenze", "pikant", "juventus", "bacon", "tarjás", "különleges", "extra", "sonkás pizza", "szalámis pizza", "magyaros pizza", "Bud Spencer", "special", "oregon", "omaha", "ünnepi", "ünnepek", "különleges"],
        "Halloween": ["halloween pizza", "halloween", "ünnepi"],
    },
    "Burger Fajták": {
        "Alap": ["burger", "alap burger", "sima burger", "hambi", "hamburger", "basic"],
        "Sajtburesz": ["sajtburesz", "cheeseburger", "sajtos burger", "cheese burger"],
        "Bacon Sajtburesz": ["bacon sajtburesz", "bacon sajtos burger", "bacon cheeseburger", "dupla bacon"],
        "BBQ": ["bbq burger", "barbecue burger", "barbeque burger"],
        "Csípős": ["csípős burger", "chili burger", "erős burger", "spicy burger"],
        "Hawaii": ["hawaii burger", "ananászos burger", "pineapple burger"],
        "Vegetáriánus": ["vegetáriánus burger", "zöldséges burger", "növényi alapú burger", "vega", "veggie", "plant-based burger"],
        "Dupla Burgerek": ["dupla burger", "dupla sajtburesz", "dupla csípős burger", "extra hús", "double burger", "dupla"],
        "King Burgerek": ["king", "whopper", "long", "special", "bacon king", "king burger"],
        "Csirkés": ["csibe burger", "csirkés burger", "chicken burger"],
    },
    "Wrap és Szendvics Típusok": {
        "Csirkés": ["csirkés wrap", "csirkés szendvics", "grillezett csirke", "chicken", "csibe wrap", "grilled chicken", "iTwist"],
        "Tonhal": ["tonhalas wrap", "tonhalas szendvics", "halas wrap", "tuna wrap", "tuna sandwich"],
        "Vegetáriánus": ["vegetáriánus wrap", "zöldséges wrap", "vegetáriánus szendvics", "vega", "vegetarian", "veggie wrap"],
        "Gyros": ["gyros wrap", "görög wrap", "tzatziki", "greek wrap"],
        "Falafel": ["falafel wrap", "csicseriborsós wrap", "vegán wrap", "chickpea wrap"],
        "Tépett Sertés": ["tépett sertés", "bbq sertés wrap", "barbecue sertés", "pulled pork wrap"],
        "Reggeli Wraps": ["qurrito", "reggeli", "deluxe toast", "háromszög szendvics", "breakfast", "melegszendvics", "morning"],
    },
    "Hagyományos Magyar Ételek": {
        "Gulyás": ["gulyás", "gulyásleves", "pörkölt", "goulash"],
        "Jókai Bableves": ["jókai bableves", "babgulyás", "bab leves", "bean soup"],
        "Tyúkhúsleves": ["tyúkhúsleves", "csirkehúsleves", "húsleves", "chicken soup"],
        "Pörkölt": ["pörkölt", "marhapörkölt", "csirkepörkölt", "sertéspörkölt", "stew"],
        "Töltött Káposzta": ["töltött káposzta", "káposztás", "savanyú káposzta", "stuffed cabbage"],
        "Lecsó": ["lecsó", "paprikás", "zöldségpörkölt", "vegetable stew", "lecsókrém", "pikáns lecsókrém"],
        "Halászlé": ["halászlé", "korhely", "fish soup"],
        "Rántott Ételek": ["rántott", "sült", "deep fried", "cordon blue", "sajt", "fried"],
        "Csülök": ["csülök", "párolt", "tócsni", "pork knuckle"],
    },
"Grillezett és Rántott Ételek": {
    "Grillezett Csirke": [
        "grillezett csirke", "sült csirke", "grilled chicken", "csirkemell filé", "csirkecomb filé",
        "chicken fillet", "csirkefalatok", "chicken strips", "pankómorzsás csirke"
    ],
    "Rántott Csirke": [
        "rántott csirke", "csirke nuggets", "csibe falatok", "chicken nuggets", "crispy chicken",
        "rántott csirkemell", "fried chicken breast", "csípős csirkeszárny", "spicy wings"
    ],
    "Sertés, Steak": [
        "grillezett sertés", "steak", "bordaszelet", "karaj", "sertésszűz", "pork steak", "bacon",
        "pankómorzsás sertés", "csontos sertésszelet", "pork fillet", "borzas borda"
    ],
    "Rántott Sertés": [
        "rántott sertés", "pankómorzsás sertés", "rántott borda", "crispy pork", "rántott karaj",
        "deep-fried pork loin", "sertés karaj rántva"
    ],
    "Grillezett Hal": [
        "grillezett hal", "grillezett tengeri", "sült hal", "grilled fish", "fogas filé", "perch fillet",
        "grillezett tengeri halfilé", "fish filet", "fish", "kemencés lazacfilé", "pisztrángfilé"
    ],
    "Rántott Hal": [
        "rántott hal", "deep-fried fish", "battered fish", "fish fillet rántva", "fogas falatok rántva",
        "fish sticks", "fish nuggets", "hal rudak", "rántott tőkehal"
    ],
    "Lazac": [
        "grillezett lazac", "lazac filé", "salmon", "roston lazacfilé", "fokhagymás lazac", "sült lazac",
        "salmon fillet", "lazac steak", "spenótos lazac", "sütőben sült lazac"
    ],
    "Rák": [
        "grillezett rák", "garnéla", "tengeri rák", "shrimp", "garnela", "garlic shrimp",
        "shrimp skewer", "grilled prawn", "garnélanyárs", "chili garnéla", "spicy shrimp"
    ],
    "Rántott Rák": [
        "rántott rák", "rántott garnéla", "deep-fried shrimp", "fried prawns", "tempura garnéla",
        "shrimp tempura", "battered shrimp", "crispy prawns", "shrimp nuggets"
    ],
    "Pisztráng és Más Halak": [
        "pisztráng", "süllő", "kecsege", "fish", "trout", "grilled trout", "whole fish",
        "kecsege filé", "zöldfűszeres süllő", "herb-crusted fish", "sült pisztráng", "kemencés hal"
    ],
    "Különféle Grillezett Ételek": [
        "grill zöldségek", "vegetable grill", "vegetable skewer", "sült zöldségek", "grillezett gomba",
        "grilled mushrooms", "pácolt zöldségek", "grillezett karfiol", "grilled cauliflower", "barbecue vegetables"
    ],
    "Rántott Zöldségek": [
        "rántott hagymakarika", "onion rings", "fried mushrooms", "rántott karfiol", "rántott gomba",
        "crispy vegetables", "rántott cukkini", "fried zucchini", "tempura zöldségek", "deep-fried veggies"
    ]
},
    "Tészta és Noodles Ételek": {
        "Spaghetti Bolognese": ["spaghetti bolognese", "húsos szósz", "spagetti", "bolognese"],
        "Carbonara": ["carbonara", "tejszínes szósz", "szalonnás tészta", "cream sauce"],
        "Lasagna": ["lasagna", "rakott tészta"],
        "Thai stílusú": ["thai tészta", "pad thai", "rizstészta", "curry tészta", "thai noodles"],
        "Kínai stílusú": ["chow mein", "lo mein", "sült tészta", "ramen", "chinese noodles"],
        "Magyar Tésztaételek": ["sztrapacska", "túrós", "csusza", "tarhonya", "hungarian pasta"],
        "Gnocchi": ["gnocchi", "pesto gnocchi", "garnéla", "gnocchi pasta", "parmezan"],
    },
    "Palacsinták és Lángosok": {
        "Édes Palacsinta": [
            "kakaós óriáspalacsinta", "kakaós palacsinta", "baracklekváros palacsinta", "nutellás óriáspalacsinta", "túrós palacsinta",
            "sweet crepe", "amerikai palacsinta", "gyümölcsös palacsinta", "turbó rudi palacsinta", "pina colada palacsinta",
            "diós-zserbós palacsinta", "mákos guba palacsinta", "nutellás-mogyorós palacsinta", "bounty palacsinta",
            "kinder palacsinta", "toffifee palacsinta", "raffaello palacsinta", "csokoládékrémes óriáspalacsinta",
            "vaníliakrémes óriáspalacsinta", "cinderella pancake", "oreo pancake", "sweetnut pancake",
            "csoki öntetes palacsinta", "eper öntetes palacsinta", "mogyorókrémes palacsinta", "fehérjepalacsinta túróval",
            "karikás-almás palacsinta", "díva palacsinta", "kanári palacsinta", "katus palacsinta", 
            "gundel palacsinta", "brutál csokis palacsinta", "túróvarázs palacsinta", "toffee palacsinta", 
            "nutellás palacsinta", "fahéjas óriáspalacsinta", "eperlekváros palacsinta", "áfonyalekváros palacsinta",
            "palacsinta patrik palacsintája", "jam palacsinta", "somlói palacsinta", "creppy palacsintapor", 
            "amerikai palacsintapor", "vitalitás palacsintapor", "barack lekváros palacsinta", 
            "palacsinta nutellás", "palacsinta ízes", "palacsinta 2 db"
        ],
        "Sós Palacsinta": [
            "palacsintás gombakrémleves", "sonkás palacsinta", "savory crepe", "hortobágyi húsos palacsinta",
            "csirkeleves palacsintacsíkokkal", "waldorf palacsinta kisadag", "alfredo palacsinta", "kofa palacsinta", 
            "csirkeleves vitalitás palacsintacsíkokkal", "finCsibe palacsinta", "vitalitás katus palacsinta"
        ],
        "Lángos": [
            "lilahagymás lángos", "vasalt lángos", "szilvalekváros lángos", "fried dough", "lángos"
        ],
    },
    "Köretek és Saláták": {
        "Köretek": ["hasábburgonya", "krumplipüré", "rizs", "burgonya", "rizi-bizi", "bulgur", "side dishes", "grillzöldség", "édesburgonyapüré", "krokett", "rösztikrokett"],
        "Saláták": ["saláta", "kert saláta", "kevert saláta", "coleslaw", "görögsaláta", "cézársaláta", "zöldsalátamix", "káposztasaláta", "paradicsomsaláta"],
        "Savanyúságok": ["savanyúság", "csemege uborka", "kovászos uborka", "pickle", "ecetes", "pickled", "uborkasaláta"],
    },
    "Szószok és Öntetek": {
        "Szószok": ["ketchup", "majonéz", "mustár", "tartármártás", "fokhagymás szósz", "édes chili", "mézes mustár", "pikáns szósz", "sauce", "édes-chili szósz", "chili szósz", "mézes-mustáros szósz", "lecsókrém", "csípős lecsókrém", "paradicsomszósz", "csípős paradicsomszósz"],
        "Öntetek": ["cézár öntet", "ezersziget", "joghurtos", "kapros", "csípős öntet", "dressing", "balzsamecetes öntet"],
        "Speciális Szószok": ["kentucky gold", "tabasco", "salsa", "bbq", "zöldfűszeres", "specialty sauce", "házi szósz"],
    },
    "Italok": {
        "Szénsavas Üdítők": ["coca-cola", "coca-cola zero", "coca cola cherry", "coca zero", "sprite", "fanta", "pepsi", "7up", "burn original", "xixo cola", "powerade", "mirinda", "canada dry", "schweppes", "kinley", "mountain dew", "somersby", "guarana energiaital", "soda", "carbonated drink", "mountaindew", "sió almalé"],
        "Jeges Tea": [
            "lipton", "fuzetea", "citromos tea", "barackos tea", "iced tea", "jeges tea", "fuze", "fuze tea", 
            "fuze zöldtea"
        ],
        "Sörök": [
            "sör", "lager", "ale", "stout", "heineken", "kronenbourg blanc", "grimbergen", "tuborg green", 
            "the beertailor", "corona", "zip's alpha wolf", "mad scientist", "ipa", "beer", "alkoholos", 
            "soproni"
        ],
        "Alkoholmentes Sörök": [
            "alcohol free", "0%", "alkoholmentes", "non-alcoholic beer"
        ],
        "Kávé és Tea": [
            "eszpresszó", "cappuccino", "latte", "koffeinmentes cappucino", "zöld tea", "fekete tea", "tejeskávé", 
            "forró csoki", "hosszú kávé", "kávé", "tea", "coffee", "koffeinmentes"
        ],
        "Gyümölcslevek": ["narancslé", "alma lé", "ananászlé", "mangólé", "szőlőlé", "multivitamin", "juice", "happy day", "cappy", "kubu", "baracklé", "topjoy", "toma", "de la vie", "regenera", "diósgyőri szeder-ribizli", "diósgyőri meggy", "diósgyőri mangó", "diósgyőri citrom"],
        "Víz": [
            "ásványvíz", "szénsavas víz", "szénsavmentes víz", "ásványi víz", "víz", "water", "naturaqua", 
            "san pellegrino", "theodora", "nature aqua"
        ],
        "Shake": [
            "shake", "shake deluxe", "pumpkin spice shake", "milkshake", "kávés shake", "vaníliaízű shake", 
            "csokoládéízű shake", "epres shake"
        ],
        "Limonádé és Szörpök": [
            "limonádé", "bodzás-limonádé", "málna-limonádé", "trópusi limonádé", "zöldalmás limonádé", 
            "creppy narancsvirág és málnaszörp", "creppy bodza és bergamott szörp", "creppy gumibogyó szörp", 
            "creppy vitalitás szörp", "slim-o-nádé"
        ],
        "Pezsgők és Borok": [
            "törley", "prosecco", "foss marai prosecco", "serena prosecco", "creppy cserszegi fűszeres", 
            "martini asti", "pezsgő", "champagne", "szénsavas bor"
        ],
        "Energizálók": [
            "burn original", "guarana energiaital", "xixo cola zero", "gatorade", "powerade", "red bull", 
            "hell", "energy drink"
        ]
    },
    "Desszertek és Édességek": {
        "Torták": [
            "csokitorta", "sacher torta", "gyümölcstorta", "krémes torta", "sajttorta", "cheesecake", 
            "cake", "dobos torta", "oreo torta", "keksz torta", "mascarponés", "vaníliás málna torta",
            "fekete erdei meggy torta", "málnás mascarpone torta", "paleo torta"
        ],
        "Fagylalt": [
            "fagyi", "fagylalt", "jégkrém", "gelato", "vanília", "csoki fagylalt", "ice cream", 
            "magnum", "ben and jerry's", "fagyasztott", "gelato", "jégkrém"
        ],
        "Pite": [
            "almás pite", "málnás pite", "meggyes pite", "gyümölcsös pite", "pie", "mákos pite", 
            "rétes", "meggyes-mákos", "almás rétes", "pite szelet"
        ],
        "Édes Péksütemények": [
            "kakaós csiga", "túrós batyu", "lekváros bukta", "fánk", "bejgli", "pastry", 
            "croissant", "kakaós-rumos", "kalács", "kifli", "linzer", "csokis", "vajkaramellás"
        ],
        "Poharas Desszertek": [
            "tiramisu", "panna cotta", "mousse", "pohárkrém", "gyümölcsös pohárdesszert", 
            "dessert cup", "profiterol", "somlói", "madártej", "gesztenyepüré", "gyümölcsrizs", "macaron"
        ],
        "Mini Desszertek": [
            "mignon", "szelet", "snickers", "macaron", "rúd", "pogácsa", "brownie", "csokis szelet", 
            "pohárdesszert", "somlói", "bonbon", "doboz", "kocka"
        ],
        "Paleo és Diétás Desszertek": [
            "paleo", "cukormentes", "lisztmentes", "diétás", "édesítőszerekkel", "zero", "gluténmentes",
            "stevia", "sütés nélküli", "fehérje"
        ]
    },
    "Különleges és Nemzetközi Konyhák": {
        "Mexikói": ["burrito", "taco", "quesadilla", "nachos", "enchilada", "mexican", "fajitas"],
        "Olasz": ["lasagna", "spaghetti", "risotto", "bruschetta", "cannoli", "italian", "gnocchi", "arrabiata"],
        "Kínai": ["tavaszi tekercs", "szecsuáni csirke", "édes-savanyú", "pekingi kacsa", "chinese", "chow mein"],
        "Japán": ["sushi", "ramen", "teriyaki", "tempura", "japanese", "miso"],
        "Indiai": ["curry", "naan", "samosa", "biriyani", "masala", "indian"],
        "Amerikai": ["hot dog", "steak", "mac and cheese", "ribs", "philly cheese steak", "american", "pumpkin spice"],
        "Görög": ["gyros", "souvlaki", "tzatziki", "moussaka", "greek", "döner"],
    },
}

# Function to classify item into category and subcategory based on keywords
def classify_item(description, item):
    for category, subcategories in categories.items():
        for subcategory, keywords in subcategories.items():
            for keyword in keywords:
                if re.search(rf'\b{keyword}\b', description, re.IGNORECASE) or re.search(rf'\b{keyword}\b', item, re.IGNORECASE):
                    return category, subcategory
    return "Egyéb", "N/A"

# Load the menu data from Excel
input_file = './menu_scraped.xlsx'
df = pd.read_excel(input_file)

# Apply classification to each row
df[['Category', 'Subcategory']] = df.apply(
    lambda row: pd.Series(classify_item(str(row['Description']), str(row['Item']))), axis=1
)

# Save the categorized data to a new Excel file
output_file = './menu_categorized_with_subcategories.xlsx'
df.to_excel(output_file, index=False)

print(f"Categorized menu with subcategories saved to: {output_file}")
