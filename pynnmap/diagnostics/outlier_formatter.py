from pynnmap.database import plot_database


class OutlierFormatter(object):

    def __init__(self, parameter_parser):
        self.parameter_parser = parameter_parser
        p = self.parameter_parser

        self.plot_db = \
            plot_database.PlotDatabase(
                p.model_type, p.model_region, p.buffer, p.model_year,
                p.image_source, p.image_version, dsn=p.plot_dsn)

    def load_outliers(self, outlier_results):
        pass


class VegclassVarietyFormatter(OutlierFormatter):
    def load_outliers(self, outlier_results):
        p = self.parameter_parser

        # Set values for constant fields
        rule_id = 'VC_VARIETY'
        variable_filter = p.get_spatial_filter()
        id_field = p.plot_id_field
        observed_value = 0.0
        predicted_value = 0.0
        vc_outlier_type = ''
        average_position = 0.0

        # Loop through outlier rows and add to DB
        for row in outlier_results:
            self.plot_db.load_outlier(
                row[id_field], rule_id, row['PREDICTION_TYPE'],
                variable_filter, observed_value, predicted_value,
                vc_outlier_type, average_position)


class VegclassOutlierFormatter(OutlierFormatter):
    def load_outliers(self, outlier_results):
        p = self.parameter_parser

        # Set values for constant fields
        rule_id = 'VC_OUTLIER'
        variable_filter = p.get_spatial_filter()
        id_field = p.plot_id_field
        average_position = 0.0

        # Loop through outlier rows and add to DB
        for row in outlier_results:
            self.plot_db.load_outlier(
                row[id_field], rule_id, row['PREDICTION_TYPE'],
                variable_filter, row['OBSERVED_VEGCLASS'],
                row['PREDICTED_VEGCLASS'], row['OUTLIER_TYPE'],
                average_position)


class NNIndexFormatter(OutlierFormatter):
    def load_outliers(self, outlier_results):
        p = self.parameter_parser

        # Set values for constant fields
        rule_id = 'NN_INDEX'
        prediction_type = 'DEPENDENT'
        variable_filter = p.get_spatial_filter()
        id_field = p.plot_id_field
        observed_value = 0.0
        predicted_value = 0.0
        vc_outlier_type = ''

        # Loop through outlier rows and add to DB
        for row in outlier_results:
            self.plot_db.load_outlier(
                row[id_field], rule_id, prediction_type, variable_filter,
                observed_value, predicted_value, vc_outlier_type,
                row['AVERAGE_POSITION'])