btn1 = {'text': '👍', 'callback_data': 'like'}
btn2 = {'text': '👎', 'callback_data': 'dislike'}
btn3 = {'text': '🆑', 'callback_data': 'remove_like'}
keyboard = [
    [btn1, btn2],
    [btn3]
]
inline_keyboard = {
    'inline_keyboard': keyboard,
}