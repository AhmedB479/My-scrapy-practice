# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        #strips all the white spaces from string
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                #value is being stripped of blank space
                adapter[field_name] = value[0].strip()

        #Category & Product Type --> switch to lower case
        lowercase_keys = ['category','product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            #lower function is being applied on the value here
            adapter[lowercase_key] = value.lower()

        #price is being converted to float annd £ is being removed
        price_keys = ['price','price_excl_tax','price_incl_tax','tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            cleaned = value.replace('£','')
            adapter[price_key] = float(cleaned)

        #availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        #split_string_array = availability_string.split('('): Splits the availability_string using '(' as the delimiter, creating an array of substrings. The assumption here is that the availability information is enclosed in parentheses.
        split_string_array = availability_string.split('(') 
        if len(split_string_array) < 2:
            #if no stock is available
            adapter['availability'] = 0
        else:
            # Splits the second part of the array (the part after the first '(') using a space as the delimiter. This is done to isolate the numeric part that represents the number of books in stock.
            availability_array = split_string_array[1].split(' ')
            # Converts the first element of the availability_array to an integer and assigns it as the value of 'availability' in the adapter dictionary. This represents the number of books in stock.
            adapter['availability'] = int(availability_array[0])
        
        #convert String --> number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)        
        
        #convert stars to int
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5
        
        
        return item
