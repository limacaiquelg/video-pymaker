from robots import input, text, image, state, video

print('>>>>> Welcome to video-pymaker! <<<<<')

state.delete_content_directory()
input.robot()
text.robot()
image.robot()
video.robot()

print('\n>>>>> Thank you for using video-pymaker! <<<<<')
