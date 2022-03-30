export const sendNewMsg = (message) => {
    return {
        type: 'ADD_NEW_MSG',
        payload: message
    }
};