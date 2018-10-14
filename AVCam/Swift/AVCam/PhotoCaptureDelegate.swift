/*
See LICENSE.txt for this sample’s licensing information.

Abstract:
Photo capture delegate.
*/

import AVFoundation
import Photos
import SwiftHTTP
import UIKit

class PhotoCaptureProcessor: NSObject {
        
	private(set) var requestedPhotoSettings: AVCapturePhotoSettings
	
	private let willCapturePhotoAnimation: () -> Void
	
	private let livePhotoCaptureHandler: (Bool) -> Void
	
	private let completionHandler: (PhotoCaptureProcessor) -> Void
	
	private var photoData: Data?
    
    private var jpegData: Data?
	
	private var livePhotoCompanionMovieURL: URL?

	init(with requestedPhotoSettings: AVCapturePhotoSettings,
	     willCapturePhotoAnimation: @escaping () -> Void,
	     livePhotoCaptureHandler: @escaping (Bool) -> Void,
	     completionHandler: @escaping (PhotoCaptureProcessor) -> Void) {
		self.requestedPhotoSettings = requestedPhotoSettings
		self.willCapturePhotoAnimation = willCapturePhotoAnimation
		self.livePhotoCaptureHandler = livePhotoCaptureHandler
		self.completionHandler = completionHandler
	}
	
	private func didFinish() {
		if let livePhotoCompanionMoviePath = livePhotoCompanionMovieURL?.path {
			if FileManager.default.fileExists(atPath: livePhotoCompanionMoviePath) {
				do {
					try FileManager.default.removeItem(atPath: livePhotoCompanionMoviePath)
				} catch {
					print("Could not remove file at url: \(livePhotoCompanionMoviePath)")
				}
			}
		}
		
		completionHandler(self)
	}
    
}

extension Data {
    struct HexEncodingOptions: OptionSet {
        let rawValue: Int
        static let upperCase = HexEncodingOptions(rawValue: 1 << 0)
    }
    
    func hexEncodedString(options: HexEncodingOptions = []) -> String {
        let format = options.contains(.upperCase) ? "%02hhX" : "%02hhx"
        return map { String(format: format, $0) }.joined()
    }
}

extension PhotoCaptureProcessor: AVCapturePhotoCaptureDelegate {
    /*
     This extension includes all the delegate callbacks for AVCapturePhotoCaptureDelegate protocol
    */
    
    func photoOutput(_ output: AVCapturePhotoOutput, willBeginCaptureFor resolvedSettings: AVCaptureResolvedPhotoSettings) {
        if resolvedSettings.livePhotoMovieDimensions.width > 0 && resolvedSettings.livePhotoMovieDimensions.height > 0 {
            livePhotoCaptureHandler(true)
        }
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, willCapturePhotoFor resolvedSettings: AVCaptureResolvedPhotoSettings) {
        willCapturePhotoAnimation()
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        
        if let error = error {
            print("Error capturing photo: \(error)")
        } else {
            photoData = photo.fileDataRepresentation()
            let uiImage = UIImage(data: photoData!)
            //let cgImage = photo.cgImageRepresentation()!.takeRetainedValue()
            //let orientation = photo.metadata[kCGImagePropertyOrientation as String] as! NSNumber
            //let uiOrientation = UIImageOrientation(rawValue: orientation.intValue)!
//            let uiimage = UIImage(cgImage: cgImage, scale: 1, orientation: uiOrientation)
            jpegData = UIImageJPEGRepresentation(uiImage!, 0.75)
        }
    }
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishRecordingLivePhotoMovieForEventualFileAt outputFileURL: URL, resolvedSettings: AVCaptureResolvedPhotoSettings) {
        livePhotoCaptureHandler(false)
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingLivePhotoToMovieFileAt outputFileURL: URL, duration: CMTime, photoDisplayTime: CMTime, resolvedSettings: AVCaptureResolvedPhotoSettings, error: Error?) {
        if error != nil {
            print("Error processing live photo companion movie: \(String(describing: error))")
            return
        }
        livePhotoCompanionMovieURL = outputFileURL
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishCaptureFor resolvedSettings: AVCaptureResolvedPhotoSettings, error: Error?) {
        if let error = error {
            print("Error capturing photo: \(error)")
            didFinish()
            return
        }
        
        //guard let photoData = photoData else {
        guard let jpegData = jpegData else {
            print("No photo data resource")
            didFinish()
            return
        }
        /* OUR CODE */
        if count < sizes.count {
            let base64Data = jpegData.base64EncodedString()
            print(count)
            print(sizes[count])
            let params = ["data": base64Data, "focal": sizes[count], "index": count, "num": sizes.count, "id": sessionId] as [String : Any]
            //let params = ["data": Upload(data: photoData, fileName: "test.jpg", mimeType: "image/jpg")]
            count = count + 1
            HTTP.POST(mainUrl+"upload", parameters: params) { response in
                // set booleans for each size and session id
                sessionStatus[sessionId] = sessionStatus[sessionId]! + 1
            }
        } else {
            print("Went over count for http post")
        }
        
    
//        func saveImage(imageName: String){
//            //create an instance of the FileManager
//            let fileManager = FileManager.default
//            //get the image path
//            let imagePath = (NSSearchPathForDirectoriesInDomains(.documentDirectory, .userDomainMask, true)[0] as NSString).appendingPathComponent(imageName)
//            //get the PNG data for this image
//            let data = UIImageJPEGRepresentation(image)
//            //store it in the document directory    fileManager.createFile(atPath: imagePath as String, contents: data, attributes: nil)
//        }
//        PHPhotoLibrary.requestAuthorization { status in
//            if status == .authorized {
//                PHPhotoLibrary.shared().performChanges({
//                    let options = PHAssetResourceCreationOptions()
//                    let creationRequest = PHAssetCreationRequest.forAsset()
//                    options.uniformTypeIdentifier = self.requestedPhotoSettings.processedFileType.map { $0.rawValue }
//                    creationRequest.addResource(with: .photo, data: photoData, options: options)
//
//                    if let livePhotoCompanionMovieURL = self.livePhotoCompanionMovieURL {
//                        let livePhotoCompanionMovieFileResourceOptions = PHAssetResourceCreationOptions()
//                        livePhotoCompanionMovieFileResourceOptions.shouldMoveFile = true
//                        creationRequest.addResource(with: .pairedVideo, fileURL: livePhotoCompanionMovieURL, options: livePhotoCompanionMovieFileResourceOptions)
//                    }
//
//                    }, completionHandler: { _, error in
//                        if let error = error {
//                            print("Error occurered while saving photo to photo library: \(error)")
//                        }
//
//                        self.didFinish()
//                    }
//                )
//            } else {
//                self.didFinish()
//            }
//        }
    }
}
