import igibson.object_states as object_states
import json
import behavior_eval
import os
import re


object_states = {
    "node_states": [
        "Cooked",
        "Dusty",
        "Frozen",
        "Open",  
        "Sliced",
        "Soaked",
        "Stained",
        "Toggled_On"
    ],
    "edge_states": [
        "Inside",
        "NextTo",
        "OnFloor",
        "OnTop",
        "Touching",
        "Under"
    ]
}
class goal_interpretation_data():
    def __init__(self):
        self.demo_to_conds_path = f"{behavior_eval.goal_int_resources_path}/data/all_conditions.json"
        self.demo_to_objs_path = f"{behavior_eval.goal_int_resources_path}/data/all_objects.json"
        self.task_to_instructions_path = f"{behavior_eval.goal_int_resources_path}/data/instructions_by_activity_name.json"
        self.prompt_path = f"{behavior_eval.goal_int_resources_path}/prompts/behavior_goal_interpretation.txt"
        self.task_to_demo_path = f"{behavior_eval.goal_int_resources_path}/data/task_to_demo.json"
        self.demo_to_prompt_path = f"{behavior_eval.goal_int_resources_path}/data/llm_prompts.json"
        
        with open(self.demo_to_conds_path, 'r') as json_file:
            self.demo_to_conds = json.load(json_file)

        with open(self.demo_to_objs_path, 'r') as json_file:
            self.demo_to_objs = json.load(json_file)

        with open(self.demo_to_prompt_path, 'r') as json_file:
            self.demo_to_prompt = json.load(json_file)

        with open(self.task_to_instructions_path, 'r') as json_file:
            self.task_to_instructions = json.load(json_file)
            
        with open(self.task_to_demo_path, 'r') as json_file:
            self.task_to_demos = json.load(json_file)

        with open(behavior_eval.demo_name_path, 'r') as file:
            self.demo_names = json.load(file)
            



        # self.all_models = [
        #     "claude-3-haiku-20240307", 
        #     "claude-3-opus-20240229", 
        #     "claude-3-sonnet-2024022", 
        #     "gemini-1.0-pro", 
        #     "gemini-1.5-flash-preview-0514", 
        #     "gemini-1.5-pro-preview-0409", 
        #     "gpt-3.5-turbo-0125", 
        #     "gpt-4-turbo-2024-04-09", 
        #     "gpt-4o-2024-05-13", 
        #     "llama-3-8b-chat", 
        #     "llama-3-70b-chat", 
        #     "mistral-large-2402", 
        #     "mixtral-8x22b-instruct-v0.1",
        #     "cohere-command-r",
        #     "cohere-command-r-plus"
        # ]


def extract_model_names(llm_response_dir):
    # List to store the extracted model names
    model_names = []

    # Get all files in the directory
    files = os.listdir(llm_response_dir)
    
    # Define a regex pattern to match the model name part of the filename
    pattern = re.compile(r"^(.*?)_outputs\.json$")
    
    for file in files:
        match = pattern.match(file)
        if match:
            # Extract the model name from the filename and add it to the list
            model_names.append(match.group(1))

    return model_names

def is_node_condition(condition):
    """check of a condition is a node condition."""
    
    # first check based on the state
    try:
        for state in object_states["node_states"]:
            if is_state_condition(state, condition):
                return True
    # if that does not work, check based on the length of the condition
    except:
        if condition[0] == "not":
            if len(condition[1]) == 2:
                return True
        else:
            if len(condition) == 2:
                return True
    return False
            
def is_edge_condition(condition):
    """check of a condition is an edge condition."""
    
    # first check based on the state
    try:
        for state in object_states["edge_states"]:
            if is_state_condition(state, condition):
                return True
                     
    # if that does not work, check based on the length of the condition
    except:
        if condition[0] == "not":
            if len(condition[1]) == 3:
                return True
        else:
            if len(condition) == 3:
                return True
    return False
    

def is_state_condition(state, condition):
    """check if the given condition is about the given state."""
    if condition[0] == 'not':
        return condition[1][0] == state.lower()
    else:
        return condition[0] == state.lower()
    

            

def compute_confusion_metrics(all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, predicted_conditions, keep_conditions=True):
    
    # Compute evaluation metrics
    true_positives = len(all_satisfied_conditions)
    false_positives = len(all_false_positive_conditions)
    false_negatives = len(all_unsatisfied_conditions)
    accuracy = true_positives / len(predicted_conditions) if predicted_conditions else 0
    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    
    if keep_conditions:
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'all_satisfied_conditions': all_satisfied_conditions,
            'all_unsatisfied_conditions': all_unsatisfied_conditions,
            'predicted_conditions': predicted_conditions,
            "false_positive_conditions": all_false_positive_conditions
        }
    else:
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }
        

# def compute_metrics_by_state(all_satisfied_conditions, all_unsatisfied_conditions, predicted_conditions):
#     """Compute metrics for each state separately."""
#     node_state_results = {}
#     edge_state_results = {}
    
#     for state in object_states["node_states"]:
#         node_state_results[state] = compute_confusion_metrics(
#             [condition for condition in all_satisfied_conditions if is_state_condition(state, condition)],
#             [condition for condition in all_unsatisfied_conditions if is_state_condition(state, condition)],
#             [condition for condition in predicted_conditions if is_state_condition(state, condition)],
#             keep_conditions=False
#         )
    
#     for state in object_states["edge_states"]:
#         edge_state_results[state] = compute_confusion_metrics(
#             [condition for condition in all_satisfied_conditions if is_state_condition(state, condition)],
#             [condition for condition in all_unsatisfied_conditions if is_state_condition(state, condition)],
#             [condition for condition in predicted_conditions if is_state_condition(state, condition)],
#             keep_conditions=False
#         )
    
#     return node_state_results, edge_state_results

# Grammatical Error Checks

def is_of_correct_length(condition):
    """check if a condition is of correct length."""
    if condition[0] == "not":
        if len(condition[1]) == 2 or len(condition[1]) == 3:
            return True
    else:
        if len(condition) == 2 or len(condition) == 3:
            return True
    # if the condition length is neither 2 nor 3, return False
    return False

def contains_valid_state(condition):
    """check if a condition contains valid state."""
    for state in object_states["node_states"]:
        if is_state_condition(state, condition):
            return True
    for state in object_states["edge_states"]:
        if is_state_condition(state, condition):
            return True
    # if the state is neither a valid node state nor a valid edge state, return False
    return False

def contains_valid_objects(condition, demo, DATA):
    """check if a conditions contains valid objects from the demo"""
    legal_objects = list(DATA.demo_to_objs[demo].keys())
    used_objects = []
    if condition[0] == "not":
        if len(condition[1]) == 2:
            used_objects.append(condition[1][1])
        elif len(condition[1]) == 3:
            used_objects.append(condition[1][1])
            used_objects.append(condition[1][2])
        else:
            assert not is_of_correct_length(condition)
            pass
    else:
        if len(condition) == 2:
            used_objects.append(condition[1])
        elif len(condition) == 3:
            used_objects.append(condition[1])
            used_objects.append(condition[2])
    
    for obj in used_objects:
        if obj not in legal_objects:
            return False
    return True



def dataset_error_analysis(all_satisfied_conditions: list, all_unsatisfied_conditions: list, all_false_positive_conditions: list, predicted_conditions: list, num_object_hallucinations: int):
    """Compute metrics for node and edge conditions separately."""
    
    grammatically_valid_predicted_conditions = []
    wrong_length = []
    state_hallucination = []
    for condition in predicted_conditions:
        if contains_valid_state(condition) and is_of_correct_length(condition):
            grammatically_valid_predicted_conditions.append(condition)
        if not is_of_correct_length(condition):
            wrong_length.append(condition)
        if not contains_valid_state(condition):
            state_hallucination.append(condition)
    
            
    node_predicted_conditions = [condition for condition in predicted_conditions if is_node_condition(condition)]
    node_satisfied_conditions = [condition for condition in all_satisfied_conditions if is_node_condition(condition)]
    node_unsatisfied_conditions = [condition for condition in all_unsatisfied_conditions if is_node_condition(condition)]
    node_false_positive_conditions = [condition for condition in all_false_positive_conditions if is_node_condition(condition)]
    edge_predicted_conditions = [condition for condition in predicted_conditions if is_edge_condition(condition)]
    edge_satisfied_conditions = [condition for condition in all_satisfied_conditions if is_edge_condition(condition)]
    edge_unsatisfied_conditions = [condition for condition in all_unsatisfied_conditions if is_edge_condition(condition)]
    edge_false_positive_conditions = [condition for condition in all_false_positive_conditions if is_edge_condition(condition)]
    
    overall_confusion = compute_confusion_metrics(all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, predicted_conditions, keep_conditions=False)
    state_confusion = compute_confusion_metrics(node_satisfied_conditions, node_unsatisfied_conditions, node_false_positive_conditions, node_predicted_conditions, keep_conditions=False)
    spatial_confusion = compute_confusion_metrics(edge_satisfied_conditions, edge_unsatisfied_conditions, edge_false_positive_conditions, edge_predicted_conditions, keep_conditions=False)
    
    return {
        'grammatical_errors': 
            {
                "grammatically_valid_num": len(grammatically_valid_predicted_conditions),
                "grammatically_valid_rate": len(grammatically_valid_predicted_conditions) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "wrong_length_num": len(wrong_length),
                "wrong_length_rate": len(wrong_length) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "state_hallucination_num": len(state_hallucination),
                "state_hallucination_rate": len(state_hallucination) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "object_hallucination_num": num_object_hallucinations,
                "object_hallucination_rate": num_object_hallucinations / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
            },
        'overall': 
            {
                "num_predicted_conditions": len(predicted_conditions),
                "num_GT_conditions": len(all_satisfied_conditions) + len(all_unsatisfied_conditions),
                "num_satisfied_conditions": len(all_satisfied_conditions),
                "num_unsatisfied_conditions": len(all_unsatisfied_conditions),
                "num_false_positive_conditions": len(all_false_positive_conditions),
                'overall_confusion_metrics': overall_confusion,
            },
        "state":
            {
                "num_predicted_conditions": len(node_predicted_conditions),
                "num_GT_conditions": len(node_satisfied_conditions) + len(node_unsatisfied_conditions),
                "num_satisfied_conditions": len(node_satisfied_conditions),
                "num_unsatisfied_conditions": len(node_unsatisfied_conditions),
                "num_false_positive_conditions": len(node_false_positive_conditions),
                'state_confusion_metrics': state_confusion,
            },
        "spatial":
            {
                "num_predicted_conditions": len(edge_predicted_conditions),
                "num_GT_conditions": len(edge_satisfied_conditions) + len(edge_unsatisfied_conditions),
                "num_satisfied_conditions": len(edge_satisfied_conditions),
                "num_unsatisfied_conditions": len(edge_unsatisfied_conditions),
                "num_false_positive_conditions": len(edge_false_positive_conditions),
                'spatial_confusion_metrics': spatial_confusion,
            },
    }




def per_demo_error_analysis(demo, all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, predicted_conditions, DATA):
    """Compute metrics for node and edge conditions separately."""
    
    grammatically_valid_predicted_conditions = []
    wrong_length = []
    state_hallucination = []
    object_hallucination = []
    for condition in predicted_conditions:
        if contains_valid_state(condition) and is_of_correct_length(condition) and contains_valid_objects(condition, demo, DATA):
            grammatically_valid_predicted_conditions.append(condition)
        if not is_of_correct_length(condition):
            wrong_length.append(condition)
        if not contains_valid_state(condition):
            state_hallucination.append(condition)
        if not contains_valid_objects(condition, demo, DATA):
            object_hallucination.append(condition)
            
    
            
    node_predicted_conditions = [condition for condition in predicted_conditions if is_node_condition(condition)]
    node_satisfied_conditions = [condition for condition in all_satisfied_conditions if is_node_condition(condition)]
    node_unsatisfied_conditions = [condition for condition in all_unsatisfied_conditions if is_node_condition(condition)]
    node_false_positive_conditions = [condition for condition in all_false_positive_conditions if is_node_condition(condition)]
    edge_predicted_conditions = [condition for condition in predicted_conditions if is_edge_condition(condition)]
    edge_satisfied_conditions = [condition for condition in all_satisfied_conditions if is_edge_condition(condition)]
    edge_unsatisfied_conditions = [condition for condition in all_unsatisfied_conditions if is_edge_condition(condition)]
    edge_false_positive_conditions = [condition for condition in all_false_positive_conditions if is_edge_condition(condition)]
    
    overall_confusion = compute_confusion_metrics(all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, predicted_conditions, keep_conditions=True)
    state_confusion = compute_confusion_metrics(node_satisfied_conditions, node_unsatisfied_conditions, node_false_positive_conditions, node_predicted_conditions, keep_conditions=True)
    spatial_confusion = compute_confusion_metrics(edge_satisfied_conditions, edge_unsatisfied_conditions, edge_false_positive_conditions, edge_predicted_conditions, keep_conditions=True)
    
    return {
        'grammatical_errors': 
            {
                "grammatically_valid_num": len(grammatically_valid_predicted_conditions),
                "grammatically_valid_rate": len(grammatically_valid_predicted_conditions) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "wrong_length_num": len(wrong_length),
                "wrong_length_rate": len(wrong_length) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "state_hallucination_num": len(state_hallucination),
                "state_hallucination_rate": len(state_hallucination) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
                "object_hallucination_num": len(object_hallucination),
                "object_hallucination_rate": len(object_hallucination) / len(predicted_conditions) if len(predicted_conditions) > 0 else 0,
            },
        'overall': 
            {
                "num_predicted_conditions": len(predicted_conditions),
                "num_GT_conditions": len(all_satisfied_conditions) + len(all_unsatisfied_conditions),
                "num_satisfied_conditions": len(all_satisfied_conditions),
                "num_unsatisfied_conditions": len(all_unsatisfied_conditions),
                "num_false_positive_conditions": len(all_false_positive_conditions),
                'overall_confusion_metrics': overall_confusion,
            },
        "state":
            {
                "num_predicted_conditions": len(node_predicted_conditions),
                "num_GT_conditions": len(node_satisfied_conditions) + len(node_unsatisfied_conditions),
                "num_satisfied_conditions": len(node_satisfied_conditions),
                "num_unsatisfied_conditions": len(node_unsatisfied_conditions),
                "num_false_positive_conditions": len(node_false_positive_conditions),
                'state_confusion_metrics': state_confusion,
            },
        "spatial":
            {
                "num_predicted_conditions": len(edge_predicted_conditions),
                "num_GT_conditions": len(edge_satisfied_conditions) + len(edge_unsatisfied_conditions),
                "num_satisfied_conditions": len(edge_satisfied_conditions),
                "num_unsatisfied_conditions": len(edge_unsatisfied_conditions),
                "num_false_positive_conditions": len(edge_false_positive_conditions),
                'spatial_confusion_metrics': spatial_confusion,
            },
    }
    


# Evaluate goals per demo

def evaluate_goals(predicted_goals, ground_truth_goals):
    """This function is in charge of figuring out the satisfied, unsatisfied, and false positive conditions"""
    # Flatten the predicted goals
    flattened_predicted_conditions = flatten_goals(predicted_goals)
    
    all_satisfied_conditions = []
    all_unsatisfied_conditions = []
    
    # check each goal in ground_truth_goals
    for key, value in ground_truth_goals.items():
        # if there is only one way to satisfy the goal
        if len(value) == 1:
            satisfied_conditions, unsatisfied_conditions = check_satisfaction(flattened_predicted_conditions, value[0])
        # if there are multiple ways to satisfy the goal, choose the one that satisfies the most number of conditions
        else:
            satisfied_nums = [len([cond for cond in option if cond in flattened_predicted_conditions]) for option in value]
            max_satisfied_option = value[satisfied_nums.index(max(satisfied_nums))]
            satisfied_conditions, unsatisfied_conditions= check_satisfaction(flattened_predicted_conditions, max_satisfied_option)
        
        all_satisfied_conditions.extend(satisfied_conditions)
        all_unsatisfied_conditions.extend(unsatisfied_conditions) 
    
    all_false_positive_conditions = [condition for condition in flattened_predicted_conditions if condition not in all_satisfied_conditions]
    
    return all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, flattened_predicted_conditions


# Basic Helper Methods

def flatten_goals(goal_data):
    """Flatten goal data into a single list of conditions."""
    return [condition for goal_type in goal_data.values() for condition in goal_type]

def check_satisfaction(predicted_conditions, ground_truth_conditions):
    """check which of the conditions in the ground truth are satisfied by the predicted conditions."""
    satisfied_conditions = []
    unsatisfied_conditions = []
    
    for condition in ground_truth_conditions:
        if condition in predicted_conditions:
            satisfied_conditions.append(condition)
        else:
            unsatisfied_conditions.append(condition)
    
    
    return satisfied_conditions, unsatisfied_conditions



# define the evaluate dataset function
def evaluate_dataset(result_reference_list, DATA):
    all_satisfied_conditions = []
    all_unsatisfied_conditions = []
    all_predicted_conditions = []
    all_false_positive_conditions = []
    
    # because it is not possible to check illegal objects for each condition without demo name
    num_object_hallucination = 0

    # this is to store results for each individual demo
    model_results_evaluated = {}
    
    for tuple in result_reference_list:
        demo = tuple["identifier"]
        goal_conds = tuple["reference"]
        model_pred = tuple["llm_output"]
        
        satisfied_conditions, unsatisfied_conditions, false_positive_conditions, flattened_predicted_conditions = evaluate_goals(model_pred, goal_conds)
        model_results_evaluated[demo] = per_demo_error_analysis(demo, satisfied_conditions, unsatisfied_conditions, false_positive_conditions, flattened_predicted_conditions, DATA)
        num_object_hallucination += model_results_evaluated[demo]["grammatical_errors"]["object_hallucination_num"]
        
        all_satisfied_conditions.extend(satisfied_conditions)
        all_unsatisfied_conditions.extend(unsatisfied_conditions)
        all_false_positive_conditions.extend(false_positive_conditions)
        all_predicted_conditions.extend(flattened_predicted_conditions)
        
        
    # save results for each individual demo
    sorted_model_results_evaluated  = {key: model_results_evaluated [key] for key in sorted(model_results_evaluated)}
    

    # this is to obtain error analysis results for the complete dataset
    dataset_results_evaluated = dataset_error_analysis(all_satisfied_conditions, all_unsatisfied_conditions, all_false_positive_conditions, all_predicted_conditions, num_object_hallucination)
    
    return dataset_results_evaluated, sorted_model_results_evaluated 


  


        



def evaluate_results(llm_response_dir, result_dir):
    '''
    This script is used to evaluate performance of the 15 LLMs in the Embodied Agents Eval Paper.
    
    ----------------------------Required Inputs----------------------------
    base prompt to be modified (prompt_path)
    relevant objects (with all possible states) (demo_to_objs_path)
    initial and goal conditions (demo_to_conds_path)
    task instructions (task_to_instructions_path)
    list of demo names (demo_names_path)
    mapping from task name to demo name (task_to_demo_path)
    -----------------------------------------------------------------------
    
    ----------------------------Produced Outputs----------------------------
    error analysis for all 15 models ({model_name}_outputs.json)
    ------------------------------------------------------------------------
    
    '''
        
        
    DATA = goal_interpretation_data()
    DATA.all_models = extract_model_names(llm_response_dir)

    ALL_RESULTS = {}

    for model_name in DATA.all_models:
        save_path = f"{llm_response_dir}/{model_name}_outputs.json"
        with open(save_path, 'r') as json_file:
            ALL_RESULTS[model_name] = json.load(json_file)

    
    ALL_METRICS = {}

    for model_name in DATA.all_models:
        model_results = ALL_RESULTS[model_name]
        
        result_reference_list = []
        for demo in DATA.demo_names:
            goal_conds = DATA.demo_to_conds[demo]['goal_conditions']
            model_pred = model_results[demo]
            # model_pred = [i for i in model_results if i['identifier'] == demo][0]['llm_output']    
            result_reference_list.append(
                {   
                    "identifier": demo,
                    "llm_output": model_pred,
                    "reference": goal_conds,
                }
            )    
        
        
        ALL_METRICS[model_name], sorted_model_results_evaluated = evaluate_dataset(result_reference_list, DATA)
        
        error_analysis_save_path = f"{result_dir}/error_analysis/{model_name}_error_analysis.json"
        os.makedirs(os.path.dirname(error_analysis_save_path), exist_ok=True)
        with open(error_analysis_save_path, 'w') as json_file:
            json.dump(sorted_model_results_evaluated, json_file, indent=4)
    
    print(f"results saved to {result_dir}/error_analysis/")

if __name__ == "__main__":
    evaluate_results()