# How DataLoader Works

Users sometimes have different sources of data. For example, one user can have their data stored in a JSON file; another user may have their data stored in an Excel file; yet another user may just want to type in all their data. Also, user's data may sometimes have different format. You have to extract, or parse the data to get what you needed for the calculation. That's what a data loader is for. A data loader takes in a data source, and parse the data into a format that is can be used in the main calculation.

If you try to write to mannually, you would have to write many calculation classes, each for a specific type of data source and format.

Instead, I use a `DataLoaderBase` class as a parent of all data loader class. This class has only one undefined method: `load_data` . Every child data loader class have to implement this method, so that it may be used later in the main calculation.

The main calculation is done in the `BonusCalculator` class. When creating an instance, this class takes in an instance of a child class (the custom data parse class that you created) of `DataLoaderBase` . `BonusCalculator` class has a method called `load_data()` , which will call the `load_data()` method of the data loader instance that you passed in.
