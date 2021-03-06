class AllMapper():

    def __init__(self, transformer_class, parameters={}):
        self.transformer = transformer_class
        self.parameters = {}


    def map(self, dataset, processed_columns, attribute_position, position_i, transformers):
        for column_i in range(len(dataset.dtypes)):
            if not column_i in processed_columns:
                new_params = self.parameters.copy()
                new_params['column_id'] = column_i
                transformers.append(self.transformer(**new_params))
                processed_columns.append(column_i)
                attribute_position[column_i] = position_i

        return processed_columns, attribute_position, transformers
