# -*- coding:utf-8 -*-
from skimage.io import imread
from skimage import color
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu,gaussian
from skimage.transform import resize
from numpy import asarray
from skimage.metrics import structural_similarity
from skimage import measure
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
from natsort import natsorted
from sklearn import linear_model, tree, ensemble
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import cv2
from scipy.signal import find_peaks

# 绘制分段数据的图形
def plot_segment(segment_df, filename):
    # 读取分段数据
    segment_data = pd.read_csv(filename)
    
    # 绘制图形
    plt.figure()
    plt.plot(segment_data['X'], label='Segment Data')
    plt.title(f'Plot for {filename}')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.show()



def crop_top_four_leads(image):
    # Load image
    # image = imread(image)
    
    # Get image dimensions
    height, width = image.shape[:2]

    # Calculate target dimensions
    

    # Crop image: assuming the top four leads occupy the top two-thirds of the image
    crop_region = (0, 0, width, int(height * 2 / 3))
    cropped_image = image[crop_region[1]:crop_region[3], crop_region[0]:crop_region[2]]

    # # Resize image
    # resized_image = cv2.resize(cropped_image, (int(target_width), int(target_height)), interpolation=cv2.INTER_AREA)

    # Save cropped and resized image
    #cv2.imwrite(output_path, resized_image)

    return cropped_image

def divide_into_leads(image):
    """
    This function divides the ECG image into 12 leads plus a long lead.
    """
	
    leads = []
    # Define the coordinates for each lead based on the typical ECG paper layout
    lead_width = image.shape[1] // 4
    lead_height = image.shape[0] // 4

    for i in range(3):
        for j in range(4):
            leads.append(image[i * lead_height:(i + 1) * lead_height, j * lead_width:(j + 1) * lead_width])

     # Last lead (long lead)
    long_lead_start = 3 * lead_height
    long_lead_end = image.shape[0]
    leads.append(image[long_lead_start:long_lead_end, :])

    return leads

def save_leads(leads, base_path):
    for i, lead in enumerate(leads):
        lead_path = f"{base_path}_lead_{i+1}.jpg"
        #cv2.imwrite(lead_path, lead)



class ECG:
	def  getImage(self,image):
		"""
		this functions gets user image
		return: user image
		"""
		
		scanned_image = imread(image)
		# cv2.imshow("Scanned", scanned_image)
		#cv2.imwrite("./image/scanned_p1.jpg", scanned_image)  # 保存扫描后的图像
		
		return scanned_image

	def GrayImage(self,image):
		"""
		This funciton converts the user image to Gray Scale
		return: Gray scale Image
		"""
		# image_gray = imread(image)
		image_gray = color.rgb2gray(image)
		# image_gray=resize(image_gray,(1572,2213))
		# image_resize=crop_top_four_leads(image)
		return image_gray

	def DividingLeads(self,image):
		"""
		This Funciton Divides the Ecg image into 13 Leads including long lead. Bipolar limb leads(Leads1,2,3). Augmented unipolar limb leads(aVR,aVF,aVL). Unipolar (+) chest leads(V1,V2,V3,V4,V5,V6)
  		return : List containing all 13 leads divided
		"""
		# Lead_1 = image[300:600, 150:643] # Lead 1
		# Lead_2 = image[300:600, 646:1135] # Lead aVR
		# Lead_3 = image[300:600, 1140:1625] # Lead V1
		# Lead_4 = image[300:600, 1630:2125] # Lead V4
		# Lead_5 = image[600:900, 150:643] #Lead 2
		# Lead_6 = image[600:900, 646:1135] # Lead aVL
		# Lead_7 = image[600:900, 1140:1625] # Lead V2
		# Lead_8 = image[600:900, 1630:2125] #Lead V5
		# Lead_9 = image[900:1200, 150:643] # Lead 3
		# Lead_10 = image[900:1200, 646:1135] # Lead aVF
		# Lead_11 = image[900:1200, 1140:1625] # Lead V3
		# Lead_12 = image[900:1200, 1630:2125] # Lead V6
		# Lead_13 = image[1250:1480, 150:2125] # Long Lead
		image_resize=crop_top_four_leads(image)
		# #All Leads in a list
		# Leads=[Lead_1,Lead_2,Lead_3,Lead_4,Lead_5,Lead_6,Lead_7,Lead_8,Lead_9,Lead_10,Lead_11,Lead_12,Lead_13]
		Leads = divide_into_leads(image_resize)
    # # Define the coordinates for each lead based on the typical ECG paper layout
	# 	Lead_width = image.shape[1] // 4
	# 	Lead_height = image.shape[0] // 4

	# 	for i in range(3):
	# 		for j in range(4):
	# 			Leads.append(image[i * Lead_height:(i + 1) * Lead_height, j * Lead_width:(j + 1) * Lead_width])

    #  # Last lead (long lead)
	# 	long_lead_start = 3 * Lead_height
	# 	long_lead_end = image.shape[0]
	# 	Leads.append(image[long_lead_start:long_lead_end, :])
		
		fig , ax = plt.subplots(4,3)
		fig.set_size_inches(10, 10)
		x_counter=0
		y_counter=0

		#Create 12 Lead plot using Matplotlib subplot

		for x,y in enumerate(Leads[:len(Leads)-1]):
			if (x+1)%3==0:
				ax[x_counter][y_counter].imshow(y)
				ax[x_counter][y_counter].axis('off')
				ax[x_counter][y_counter].set_title("Leads {}".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax[x_counter][y_counter].imshow(y)
				ax[x_counter][y_counter].axis('off')
				ax[x_counter][y_counter].set_title("Leads {}".format(x+1))
				y_counter+=1
	    
		#save the image
		fig.savefig('Leads_1-12_figure.jpg')
		fig1 , ax1 = plt.subplots()
		fig1.set_size_inches(10, 10)
		ax1.imshow(Leads[12])
		ax1.set_title("Leads 13")
		ax1.axis('off')
		fig1.savefig('Long_Lead_13_figure.jpg')

		return Leads

	def PreprocessingLeads(self,Leads):
		"""
		This Function Performs preprocessing to on the extracted leads.
		"""
		fig2 , ax2 = plt.subplots(4,3)
		fig2.set_size_inches(10, 10)
		#setting counter for plotting based on value
		x_counter=0
		y_counter=0

		for x,y in enumerate(Leads[:len(Leads)-1]):
			 # Ensure the image has 3 channels (RGB)
			if y.ndim == 2:
            # If the image is already grayscale, we can directly use it
				grayscale = y
			elif y.ndim == 3 and y.shape[2] == 3:
            # Convert RGB to grayscale
				grayscale = color.rgb2gray(y)
			else:
				raise ValueError("Input image must be either a 2D grayscale or a 3D RGB image")
			#smoothing image
			blurred_image = gaussian(grayscale, sigma=1)
			#thresholding to distinguish foreground and background
			#using otsu thresholding for getting threshold value
			global_thresh = threshold_otsu(blurred_image)

			#creating binary image based on threshold
			binary_global = blurred_image < global_thresh
			#resize image
			#binary_global = resize(binary_global, (300, 450))
			if (x+1)%3==0:
				ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
				ax2[x_counter][y_counter].axis('off')
				ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
				ax2[x_counter][y_counter].axis('off')
				ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
				y_counter+=1
		fig2.savefig('Preprossed_Leads_1-12_figure.png')

		#plotting lead 13
		fig3 , ax3 = plt.subplots()
		fig3.set_size_inches(10, 10)
		# Ensure the image has 3 channels (RGB)
		if Leads[-1].ndim == 2:
        # If the image is already grayscale, we can directly use it
			grayscale = Leads[-1]
		elif Leads[-1].ndim == 3 and Leads[-1].shape[2] == 3:
        # Convert RGB to grayscale
			grayscale = color.rgb2gray(Leads[-1])
		else:
			raise ValueError("Input image must be either a 2D grayscale or a 3D RGB image")
		
		blurred_image = gaussian(grayscale, sigma=1)
		#thresholding to distinguish foreground and background
		#using otsu thresholding for getting threshold value
		global_thresh = threshold_otsu(blurred_image)
		print(global_thresh)
		#creating binary image based on threshold
		binary_global = blurred_image < global_thresh
		ax3.imshow(binary_global,cmap='gray')
		ax3.set_title("Leads 13")
		ax3.axis('off')
		fig3.savefig('Preprossed_Leads_13_figure.png')


	def SignalExtraction_Scaling(self,Leads):
		"""
		This Function Performs Signal Extraction using various steps,techniques: conver to grayscale, apply gaussian filter, thresholding, perform contouring to extract signal image and then save the image as 1D signal
		"""
		fig4 , ax4 = plt.subplots(4,3)
		#fig4.set_size_inches(10, 10)
		x_counter=0
		y_counter=0
		for x,y in enumerate(Leads[:len(Leads)-1]):
    	# Check if y is grayscale or RGB
			if len(y.shape) == 3 and y.shape[2] == 3:
				grayscale = color.rgb2gray(y)
			else:
				grayscale = y  # Assume already grayscale
    # Remaining code remains the same...

			#smoothing image
			blurred_image = gaussian(grayscale, sigma=0.7)
			#thresholding to distinguish foreground and background
			#using otsu thresholding for getting threshold value
			global_thresh = threshold_otsu(blurred_image)

			#creating binary image based on threshold
			binary_global = blurred_image < global_thresh
			#resize image
			binary_global = resize(binary_global, (300, 450))
			#finding contours
			contours = measure.find_contours(binary_global,0.8)
			contours_shape = sorted([x.shape for x in contours])[::-1][0:1]
			for contour in contours:
				if contour.shape in contours_shape:
					test = resize(contour, (255, 2))
			if (x+1)%3==0:
				ax4[x_counter][y_counter].invert_yaxis()
				ax4[x_counter][y_counter].plot(test[:, 1], test[:, 0],linewidth=1,color='black')
				ax4[x_counter][y_counter].axis('image')
				ax4[x_counter][y_counter].set_title("Contour {} image".format(x+1))
				x_counter+=1
				y_counter=0
			else:
				ax4[x_counter][y_counter].invert_yaxis()
				ax4[x_counter][y_counter].plot(test[:, 1], test[:, 0],linewidth=1,color='black')
				ax4[x_counter][y_counter].axis('image')
				ax4[x_counter][y_counter].set_title("Contour {} image".format(x+1))
				y_counter+=1
	    
			#scaling the data and testing
			lead_no=x
			scaler = MinMaxScaler()
			fit_transform_data = scaler.fit_transform(test)
			Normalized_Scaled=pd.DataFrame(fit_transform_data[:,0], columns = ['X'])
			Normalized_Scaled=Normalized_Scaled.T
			#scaled_data to CSV
			if (os.path.isfile('scaled_data_1D_{lead_no}.csv'.format(lead_no=lead_no+1))):
				Normalized_Scaled.to_csv('Scaled_1DLead_{lead_no}.csv'.format(lead_no=lead_no+1), mode='a',index=False)
			else:
				Normalized_Scaled.to_csv('Scaled_1DLead_{lead_no}.csv'.format(lead_no=lead_no+1),index=False)
	      	# Save original data to CSV in a separate folder
		
		fig4.savefig('Contour_Leads_1-12_figure.png')

# 	def Segmentingcycles(self):
# 		for i in range(1, 13):
# 			filename = f'Scaled_1DLead_{i}.csv'
# 			if not os.path.exists(filename):
# 				continue
# 			# Transpose the dataframe to convert columns to rows
# 			df1 = pd.read_csv(filename)
# 			df1_t = df1.T

# # Reset index to convert the index to a column and make it a regular column
# 			df1_t.reset_index(drop=True, inplace=True)

# # Rename the column to 'X' to match the format of the second file
# 			df1_t.columns = ['X']

# # Save the transformed dataframe to a new CSV file
# 			output_path = '/old_home/lyt/zxj_workplaces/Cardiovascular-Detection-using-ECG-images-main/Deployment/Scaled_X_{i}.csv'
# 			df1_t.to_csv(output_path, index=False)

# 			df = pd.read_csv(output_path)
# 			fig, ax = plt.subplots()
# 			plt.gca().invert_yaxis()
# 			ax.plot(df, linewidth=1, color='black', linestyle='solid')
# 			peaks, _ = find_peaks(-df['X'])

# # Extract local minima points
# 			local_minima = df.iloc[peaks]

# # Sort local minima by value
# 			local_minima_sorted = local_minima.sort_values(by='X')

# # Get the top four local minima indexes (sorted)
# 			top_four_indexes = local_minima_sorted.head(4).index.tolist()
# 			min_value = df['X'].min()
# 			local_minima_filtered = [index for index in top_four_indexes if df.at[index, 'X'] < (min_value +0.1)]

# # Sort the filtered indexes to maintain the order
# 			sorted_indexes = sorted(local_minima_filtered)

# 			print("Top  local minima indexes (sorted and filtered):", sorted_indexes)
# 			for index in sorted_indexes:
# 				ax.axvline(x=index, color='red', linestyle=':')

# # For your other variables left, middle, right, and last, you will need to recalculate them based on the filtered indexes
# 			left = sorted_indexes[0] if sorted_indexes else None
# 			middle = sorted_indexes[1] if len(sorted_indexes) > 1 else None
# 			right = sorted_indexes[2] if len(sorted_indexes) > 2 else None
# 			last = sorted_indexes[-1] if len(sorted_indexes)>3 else None
# 			if len(sorted_indexes) == 3:
    
#     # Calculate the values of the local minima
# 				left_value = df.loc[left]['X']
# 				middle_value = df.loc[middle]['X']
# 				right_value = df.loc[right]['X']
# 				print("Left, middle, and right values:", left_value, middle_value, right_value)
    
# 				mid_1_2_pos = left + (middle - left) * 2 / 3
# 				mid_2_3_pos = middle + (right - middle) * 2 / 3
        
#         # Plot vertical lines at the calculated positions
# 				ax.axvline(x=mid_1_2_pos, color='blue', linestyle='--')
# 				ax.axvline(x=mid_2_3_pos, color='blue', linestyle='--')
        
# 				print("Blue line positions (case 1):", mid_1_2_pos, mid_2_3_pos)
# 				segment2_case2 = df.loc[mid_1_2_pos+1:mid_2_3_pos]
# 				segment2_case2.to_csv('segment2_case2.csv', index=False)
				
        

# 				left_0_1_pos = left - (middle - left) / 3
# 				left_1_2_pos = left + (middle - left) * 2 / 3
# 				right_2_3_pos = right - (right - middle) / 3
# 				right_3_4_pos = right + (right - middle) * 2 / 3

#         # Check if calculated positions are within the range, then draw blue lines
# 				if left_0_1_pos >= 0 and left_1_2_pos <= middle:
# 					ax.axvline(x=left_0_1_pos, color='blue', linestyle='--')
# 					ax.axvline(x=left_1_2_pos, color='blue', linestyle='--')
# 					segment1_case2 = df.loc[left_0_1_pos+1:left_1_2_pos]
# 					segment1_case2.to_csv('segment1_case2.csv', index=False)
# 					plot_segment(segment1_case2, 'segment1_case2.csv')

# 				if right_2_3_pos <= right and right_3_4_pos <= len(df):
# 					ax.axvline(x=right_2_3_pos, color='blue', linestyle='--')
# 					ax.axvline(x=right_3_4_pos, color='blue', linestyle='--')
# 					segment3_case2 = df.loc[right_2_3_pos+1:right_3_4_pos]
# 					segment3_case2.to_csv('segment3_case2.csv', index=False)
# 					plot_segment(segment3_case2, 'segment3_case2.csv')
# 				print("Left blue line positions (case 1):", left_0_1_pos, left_1_2_pos)
# 				print("Right blue line positions (case 1):", right_2_3_pos, right_3_4_pos)

# 				plot_segment(segment2_case2, 'segment2_case2.csv')
# 			elif len(sorted_indexes) == 4:       
# 				left_value = df.loc[left]['X']
# 				middle_value = df.loc[middle]['X']
# 				right_value = df.loc[right]['X']
# 				last_value = df.loc[last]['X']
# 				print("Left, middle, right and last values:", left_value, middle_value, right_value,last_value)
    
#     # If the difference between the first two and the second two values is less than 10, execute this condition
    
# 				mid_1_2_pos = left + (middle - left) * 2 / 3
# 				mid_2_3_pos = middle + (right - middle) * 2 / 3
# 				right_2_3_pos = right - (right - middle) / 3
# 				right_3_4_pos = right + (right - middle) * 2 / 3

#         # Plot vertical lines at the calculated positions
# 				ax.axvline(x=mid_1_2_pos, color='blue', linestyle='--')
# 				ax.axvline(x=mid_2_3_pos, color='blue', linestyle='--')
# 				ax.axvline(x=right_2_3_pos, color='blue', linestyle='--')
# 				ax.axvline(x=right_3_4_pos, color='blue', linestyle='--') 

# 				print("Blue line positions :", mid_1_2_pos, mid_2_3_pos)
# 				segment2_case2 = df.loc[mid_1_2_pos+1:mid_2_3_pos]
# 				segment2_case2.to_csv('segment2_case2.csv', index=False)
#     # plot_segment(segment2_case2, 'segment3_case2.csv') 
# 				print("Right blue line positions :", right_2_3_pos, right_3_4_pos)
# 				segment3_case2 = df.loc[right_2_3_pos+1:right_3_4_pos]
# 				segment3_case2.to_csv('segment3_case2.csv', index=False)
# 				plot_segment(segment3_case2, 'segment3_case2.csv')    

# 				left_0_1_pos = left - (middle - left) / 3
# 				left_1_2_pos = left + (middle - left) * 2 / 3
    
# 				last_3_4_pos = last - (last-right)/3
# 				last_4_5_pos = last + (last-right)*2/3

# 				if left_0_1_pos >= 0 and left_1_2_pos <= middle:
# 					ax.axvline(x=left_0_1_pos, color='blue', linestyle='--')
# 					ax.axvline(x=left_1_2_pos, color='blue', linestyle='--')
# 					segment1_case2 = df.loc[left_0_1_pos+1:left_1_2_pos]
# 					segment1_case2.to_csv('segment1_case2.csv', index=False)
# 					plot_segment(segment1_case2, 'segment1_case2.csv')

# 				if last_3_4_pos <= last and last_4_5_pos <= len(df):
# 					ax.axvline(x=last_3_4_pos, color='blue', linestyle='--')
# 					ax.axvline(x=last_4_5_pos, color='blue', linestyle='--')
# 					segment5_case2 = df.loc[last_3_4_pos+1:last_4_5_pos]
# 					segment5_case2.to_csv('segment5_case2.csv', index=False)
# 					plot_segment(segment5_case2, 'segment5_case2.csv')
        
# 				print("Left blue line positions :", left_0_1_pos, left_1_2_pos)
# 				print("Last blue line positions :", last_3_4_pos, last_4_5_pos)     
        
# 				plot_segment(segment2_case2, 'segment2_case2.csv')
# 			elif len(sorted_indexes) == 2:
# 				two_arr=[left, middle]
# 				dist=middle-left
# 				f_0_1_pos=left-dist/3
# 				f_1_2_pos=left+dist*2/3
# 				s_1_2_pos=middle-dist/3
# 				s_2_3_pos=middle+dist*2/3
        
# 				print("Left blue line positions (case 2):", f_0_1_pos, f_1_2_pos)
# 				print("Right blue line positions (case 2):", s_1_2_pos, s_2_3_pos)

#         # Check if calculated positions are within the range, then draw blue lines
# 				if f_0_1_pos >= 0 and f_1_2_pos <= middle:
# 					ax.axvline(x=f_0_1_pos, color='blue', linestyle='--')
# 					ax.axvline(x=f_1_2_pos, color='blue', linestyle='--')
# 					segment1_case2 = df[(df.index >= f_0_1_pos) & (df.index <= f_1_2_pos)]
# 					segment1_case2.to_csv('segment1_case2.csv', index=False)
# 				if s_1_2_pos <= right and s_2_3_pos <= len(df):
# 					ax.axvline(x=s_1_2_pos, color='blue', linestyle='--')
# 					ax.axvline(x=s_2_3_pos, color='blue', linestyle='--')
# 					segment2_case2 = df[(df.index > s_1_2_pos) & (df.index <= s_2_3_pos)]
# 					segment2_case2.to_csv('segment2_case2.csv', index=False)
        
# 				plot_segment(segment1_case2, 'segment1_case2.csv')
# 				plot_segment(segment2_case2, 'segment2_case2.csv')
        
        
# 			else:
# 				print("Not enough local minima points to calculate positions.")

# # Show the plot
# 			plt.show()

	def CombineConvert1Dsignal(self):
		"""
		This function combines all 1D signals of 12 Leads into one FIle csv for model input.
		returns the final dataframe
		"""
		#first read the Lead1 1D signal
		test_final=pd.read_csv('Scaled_1DLead_1.csv')
		location= os.getcwd()
		print(location)
		#loop over all the 11 remaining leads and combine as one dataset using pandas concat
		for files in natsorted(os.listdir(location)):
			if files.endswith(".csv"):
				if files!='Scaled_1DLead_1.csv':
					df=pd.read_csv('{}'.format(files))
					test_final=pd.concat([test_final,df],axis=1,ignore_index=True)

		return test_final
		
	def DimensionalReduciton(self,test_final):
		"""
		This function reduces the dimensinality of the 1D signal using PCA
		returns the final dataframe
		"""
		#first load the trained pca
		pca_loaded_model = joblib.load(r'/old_home/lyt/zxj_workplaces/Cardiovascular-Detection-using-ECG-images-main/model_pkl/PCA_ECG (1).pkl')
		result = pca_loaded_model.transform(test_final)
		final_df = pd.DataFrame(result)
		return final_df

	def ModelLoad_predict(self,final_df):
		"""
		This Function Loads the pretrained model and perfrom ECG classification
		return the classification Type.
		"""
		loaded_model = joblib.load(r'/old_home/lyt/zxj_workplaces/Cardiovascular-Detection-using-ECG-images-main/model_pkl/Heart_Disease_Prediction_using_ECG (4).pkl')
		result = loaded_model.predict(final_df)
		if result[0] == 1:
			return "Your ECG corresponds to Myocardial Infarction\n您的心电图显示心肌梗死"
		elif result[0] == 0:
			return "Your ECG corresponds to Abnormal Heartbeat\n您的心电图显示心律异常"
		elif result[0] == 2:
			return "Your ECG is Normal\n您的心电图正常"
		else:
			return "Your ECG corresponds to History of Myocardial Infarction\n您的心电图显示出心肌梗死的历史记录"
