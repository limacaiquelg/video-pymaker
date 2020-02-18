from robots import state, input, text, image, video, youtube

print('>>>>> Welcome to video-pymaker! <<<<<')

state.delete_content_directory()
input.robot()
text.robot()
image.robot()
video.robot()
youtube.robot()

print('\n>>>>> Thank you for using video-pymaker! <<<<<')
