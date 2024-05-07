#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
import pandas as pd
processed_exercise_data = process_exercise_data(exercises_df)

app = Flask(__name__)

# Ensure you load your processed_exercise_data correctly here
# processed_exercise_data = pd.read_csv('path_to_your_data.csv')

def get_exercises_by_muscle(processed_data, muscle):
    muscle = muscle.lower()  # Convert the muscle parameter to lowercase
    # Filter exercises that involve the specified muscle
    # Checking if the muscle is in any of the list's elements, accounting for case
    result = processed_data[processed_data['muscles_involved'].apply(lambda x: any(muscle in m.lower() for m in x))]
    return result

@app.route('/exercises', methods=['GET'])
def exercises_by_muscle():
    muscle = request.args.get('muscle', None)
    if not muscle:
        return jsonify({'error': 'Muscle parameter is required'}), 400
    try:
        result = get_exercises_by_muscle(processed_exercise_data, muscle)
        if result.empty:
            return jsonify({'message': 'No exercises found for the given muscle'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app, use_reloader=False)


# In[3]:




