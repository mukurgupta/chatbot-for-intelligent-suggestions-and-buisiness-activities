import {combineReducers} from 'redux';
import messages from "./messages";

const reducers = combineReducers({
    messages:messages,
});

export default reducers;