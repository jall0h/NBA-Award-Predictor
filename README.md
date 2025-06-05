# NBA Awards Predictor

This project aims to predict the winners of the NBA Awards for MVP, DPOY, ROTY, and 6MOTY using only player statistics.

# Install
```
pip install requirements.txt
```

## Challenges, Future Work and Improvements

### Challenges
The data is imbalanced as only one player is given each award at the end of the season. The model was evaluated using F1-score and Precision. This project failed to account for the voting-based system for these awards, which would have resulted in using a regression model for ranking rather than a classification model. The classification models evaluated poorly.

### Future Work and Improvements
- Use of a classification Model
- Use the previous MVP data selection
- Add Team statistics
- Glaze Glorious Goat Lebron James
