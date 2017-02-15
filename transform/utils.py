# Treating categorical variable.Converting to numeric to make them usable

# doing feature scaling by subtracting mean of (21.5,29.5,39.5,49.5,59.5,65) i,e., 44 / std deviation i,e., 17


def age_conversion(age):
    if age == "19-24":
        return 21.5
    if age == "25-34":
        return 29.5
    if age == "35-44":
        return 39.5
    if age == "45-54":
        return 49.5
    if age == "55-64":
        return 59.5
    if age == "65+":
        return 65
    return 39.5  # if null return the category with max frequency


def household_size_conversion(hh_size):
    if hh_size == "1":
        return 1
    if hh_size == "2":
        return 2
    if hh_size == "3":
        return 3
    if hh_size == "4":
        return 4
    if hh_size == "5+":
        return 5
    return 2  # if null return the category with max frequency


# Creating a new income variable for each customer which is equal to the mean of the income bucket the customer falls in
# doing feature scaling by subtracting mean of (7500, 19500, 29500, 42000, 62000, 87000, 112000, 137000, 164000, 187000,
#  224500) i,e., 97454 / std deviation i,e., 73205
def income_conversion(income):
    if income == "Under 15K":
        return 7500
    if income == "15-24K":
        return 19500
    if income == "25-34K":
        return 29500
    if income == "35-49K":
        return 42000
    if income == "50-74K":
        return 62000
    if income == "75-99K":
        return 87000
    if income == "100-124K":
        return 112000
    if income == "125-149K":
        return 137000
    if income == "150-174K":
        return 164000
    if income == "175-199K":
        return 187000
    if income == "200-249K":
        return 224500
    if income == "250K+":
        return 250000
    return 62000  # if income is not in any of these categories, replacing with most frequent category


popularCommodity = ['SOFT DRINKS',
                    'BEEF',
                    'FLUID MILK PRODUCTS',
                    'CHEESE',
                    'FRZN MEAT/MEAT DINNERS',
                    'BAG SNACKS',
                    'BEERS/ALES',
                    'FROZEN PIZZA',
                    'BAKED BREAD/BUNS/ROLLS',
                    'COLD CEREAL',
                    'CIGARETTES',
                    'CHICKEN',
                    'LUNCHMEAT',
                    'PORK',
                    'SOUP',
                    'ICE CREAM/MILK/SHERBTS'
                    ]

invalidProducts = [5126106, 5993055, 5978657, 5126087, 5993051, 5978650, 5978659, 6693056, 5993054, 5126088, 5126107,
                   5978649, 5977100, 5978656, 5978648]

invalidDepartment = ['CHARITABLE CONT', 'CNTRL/STORE SUP', 'DELI/SNACK BAR', 'ELECT &PLUMBING', 'GRO BAKERY', 'HBC',
                     'HOUSEWARES', 'MEAT-WHSE', 'PHARMACY SUPPLY', 'PHOTO', 'PORK', 'POSTAL CENTER', 'PROD-WHS',
                     'SALES', 'RX', 'TOYS', 'VIDEO', 'VIDEO RENTAL', 'AUTOMOTIVE', 'DAIRY DELI', 'GM MERCH EXP',
                     'PROD-WHS SALES']

validDepartment = ['DRUG GM', 'GROCERY', 'KIOSK-GAS', 'MEAT', 'MEAT-PCKGD', 'PRODUCE']
