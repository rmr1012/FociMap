// swift-tools-version:4.0

import PackageDescription

let package = Package(
    name: "AVCam",
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "4.0.0")
        ],
    targets: [
        .target(
            name: "AVCam",
            dependencies: ["Alamofire"]
        ),
        ]
)
