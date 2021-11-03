from datetime import datetime, timedelta


def get_week(date):
    today = datetime.strptime(date, '%Y-%m-%d').date()

    if today.weekday() == 0:
        monday = today
        tuesday = today + timedelta(days=1)
        wednesday = today + timedelta(days=2)
        thursday = today + timedelta(days=3)
        friday = today + timedelta(days=4)
        saturday = today + timedelta(days=5)
        sunday = today + timedelta(days=6)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday), ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week

    elif today.weekday() == 1:
        tuesday = today
        monday = today - timedelta(days=1)
        wednesday = today + timedelta(days=1)
        thursday = today + timedelta(days=2)
        friday = today + timedelta(days=3)
        saturday = today + timedelta(days=4)
        sunday = today + timedelta(days=5)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week


    elif today.weekday() == 2:
        wednesday = today
        monday = today - timedelta(days=2)
        tuesday = today - timedelta(days=1)
        thursday = today + timedelta(days=1)
        friday = today + timedelta(days=2)
        saturday = today + timedelta(days=3)
        sunday = saturday + timedelta(days=4)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week


    elif today.weekday() == 3:
        thursday = today
        monday = today - timedelta(days=3)
        tuesday = today - timedelta(days=2)
        wednesday = today - timedelta(days=1)
        friday = today + timedelta(days=1)
        saturday = today + timedelta(days=2)
        sunday = saturday + timedelta(days=3)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week


    elif today.weekday() == 4:
        friday = today
        monday = today - timedelta(days=4)
        tuesday = today - timedelta(days=3)
        wednesday = today - timedelta(days=2)
        thursday = today - timedelta(days=1)
        saturday = today + timedelta(days=1)
        sunday = today + timedelta(days=2)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week


    elif today.weekday() == 5:
        saturday = today
        monday = today - timedelta(days=5)
        tuesday = today - timedelta(days=4)
        wednesday = today - timedelta(days=3)
        thursday = today - timedelta(days=2)
        friday = today - timedelta(days=1)
        sunday = today + timedelta(days=1)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}
        return week

    elif today.weekday() == 6:
        sunday = today
        monday = today - timedelta(days=6)
        tuesday = today - timedelta(days=5)
        wednesday = today - timedelta(days=4)
        thursday = today - timedelta(days=3)
        friday = today - timedelta(days=3)
        saturday = today - timedelta(days=1)

        week = {key: value for (key, value) in (
            ('monday', monday), ('tuesday', tuesday),  ('wednesday', wednesday), ('thursday', thursday),
            ('friday', friday), ('saturday', saturday), ('sunday', sunday))}

        return week