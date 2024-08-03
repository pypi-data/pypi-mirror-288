import unittest
from pucktrick.noisy import * 
import pandas as pd
from pandas.testing import assert_frame_equal
class TestCategorical(unittest.TestCase):
    def test_saluta(self):
        percentage=0.5
        num_rows = 1000
        fake_df=create_fake_table()
        column='f2'
        noise_df=noiseCategoricalStringNewFakeValues(fake_df,column,percentage)
        print(noise_df)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        noise_df=noiseCategoricalStringExstendedFakeValues(fake_df,noise_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        diff_p=diff_number/num_rows
    
        # Verifica che il numero di modifiche sia corretto
        self.assertEqual(diff_p, percentage)
    

def create_fake_table():
  num_rows = 1000
  # Generate data for each column
  f1 = np.random.uniform(-100, 100, num_rows)  # Continuous values between -100 and 100
  f2 = np.random.randint(-100, 101, num_rows)  # Discrete values between -100 and 100
  f3 = np.random.choice(['apple', 'banana', 'cherry'], num_rows)  # String values
  f4 = np.random.choice(['apple', 'banana', 'cherry'], num_rows)  # String values
  f5 = np.random.choice([0, 1], num_rows)  # Binary values (0 or 1)
  target = np.random.choice([0, 1], num_rows)  # Binary target (0 or 1)

  # Create the DataFrame
  df = pd.DataFrame({
    'f1': f1,
    'f2': f2,
    'f3': f3,
    'f4': f4,
    'f5': f5,
    'target': target
  })
  return df

if __name__ == "__main__":
    unittest.main()
