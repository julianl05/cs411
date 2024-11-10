#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5002/api"

# Flag to control whether to echo JSON output
ECHO_JSON=true

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
# Healthchecks
###############################################

check_health() {
  echo "Checking health status..."
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    echo "$response"
    exit 1
  fi
}

check_db() {
  echo "Checking database connection..."
  response=$(curl -s -X GET "$BASE_URL/db-check")
  if echo "$response" | grep -q '"database_status": "healthy"'; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    echo "$response"
    exit 1
  fi
}

###############################################
# Meals Management
###############################################

clear_meals() {
  echo "Clearing the meals..."
  response=$(curl -s -X DELETE "$BASE_URL/clear-meals")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meals cleared successfully."
  else
    echo "Failed to clear meals."
    echo "$response"
    exit 1
  fi
}

create_meal() {
  meal=$1
  cuisine=$2
  price=$3
  difficulty=$4

  echo "Adding meal ($meal, $cuisine, $price, $difficulty)..."
  response=$(curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    echo "$response"
    exit 1
  fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    echo "$response"
    exit 1
  fi
}

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    echo "$response"
    exit 1
  fi
}

get_meal_by_name() {
  meal_name=$(echo $1 | sed 's/ /%20/g')  # URL encode the meal name

  echo "Getting meal by name ($1)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal_name")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meal retrieved successfully by name."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by name."
    echo "$response"
    exit 1
  fi
}

###############################################
# Battle
###############################################

start_battle() {
  echo "Starting a meal battle..."
  response=$(curl -s -X GET "$BASE_URL/battle")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Meal battle started successfully."
  else
    echo "Failed to start meal battle."
    echo "$response"
    exit 1
  fi
}

clear_combatants() {
  echo "Clearing combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear combatants."
    echo "$response"
    exit 1
  fi
}

get_combatants() {
  echo "Getting combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Combatants retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get combatants."
    echo "$response"
    exit 1
  fi
}

prep_combatant() {
  meal=$1

  echo "Preparing combatant: $meal"
  response=$(curl -s -X POST "$BASE_URL/prep-combatant" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\"}")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Combatant prepared successfully."
    get_combatants
  else
    echo "Failed to prepare combatant."
    echo "$response"
    exit 1
  fi
}

###############################################
# Leaderboard
###############################################

get_leaderboard() {
  sort_by=$1

  echo "Getting leaderboard sorted by $sort_by..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=$sort_by")
  echo "$response" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard."
    echo "$response"
    exit 1
  fi
}

###############################################
# Execute Tests
###############################################

# Health checks
check_health
check_db

clear_meals
create_meal "Spaghetti Carbonara" "Italian" 20 "MED"
create_meal "Beef Bulgogi" "Korean" 35 "HIGH"
create_meal "Sushi" "Japanese" 15 "LOW"
create_meal "Foie Gras" "French" 100 "LOW"

delete_meal_by_id 1

get_meal_by_id 2
get_meal_by_id 3
get_meal_by_id 4
get_meal_by_name "Beef Bulgogi"
get_meal_by_name "Sushi"
get_meal_by_name "Foie Gras"

clear_meals

create_meal "Spaghetti Carbonara" "Italian" 20 "MED"
create_meal "Beef Bulgogi" "Korean" 35 "HIGH"
create_meal "Sushi" "Japanese" 15 "LOW"
create_meal "Foie Gras" "French" 100 "LOW"

clear_combatants
prep_combatant "Beef Bulgogi"
prep_combatant "Sushi"
start_battle

clear_combatants
prep_combatant "Beef Bulgogi"
prep_combatant "Foie Gras"
clear_combatants
prep_combatant "Sushi"
prep_combatant "Foie Gras"
start_battle

get_leaderboard "wins"
get_leaderboard "win_pct"

clear_combatants
prep_combatant "Beef Bulgogi"
prep_combatant "Foie Gras"
start_battle

get_leaderboard "wins"
get_leaderboard "win_pct"

#keep the previous winner, fight a third combatant
prep_combatant "Sushi"
start_battle

get_leaderboard "wins"
get_leaderboard "win_pct"

echo "All tests passed successfully!"
