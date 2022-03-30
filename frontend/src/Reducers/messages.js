const initialState = [];

export default function (state = initialState, action) {
    switch(action.type){
        case 'ADD_NEW_MSG':
        		return [...state, action.payload];
        default:
            return state;
    }
}