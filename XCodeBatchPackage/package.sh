 #!/bin/bash

#base config
project_name="" #GarlicObject
team_id="" #xxxxxxxxxx
project_path="" #/Users/garlic/iOS/GarlicObject
resource_path="" #/Users/garlic/GitHub/EasyScript/XCodeBatchPackage/Resources
export_plist_path="" #/Users/garlic/GitHub/EasyScript/XCodeBatchPackage/Export.plist
archive_path="" #/Users/garlic/GitHub/EasyScript/XCodeBatchPackage/Archive
output_path="" #/Users/garlic/GitHub/EasyScript/XCodeBatchPackage/Output
build_temp_path="" #/Users/garlic/GitHub/EasyScript/XCodeBatchPackage/Temp

#projcts resources dir
resourceNames=(Project_01 Project_02 Project_03)

appNames=(Project_01 Project_02 Project_03) #CFBundleDisplayName CFBundleName
bidPrefix="" #bidPrefix like:com.garlic.
appIds=(Project_01 Project_02 Project_03) #bidSuffix

AppIconsDir="AppIcons"
icon_image_name="AppIcon.png"
icon_array=(20 29 40 58 60 76 80 87 120 152 167 180 1024) #icon size

changeNames=(AboutUs LaunchScreen) #dir or file
changeNamesInProj=(Resource/Images Resource/Images) #dir or file

currentAppName=""
currentAppId=""
MWConfiguration=Debug #Debug Release
MWBuildTempDir=""


prepare() {
    projcet_reousrce_path="$resource_path/$currentAppName"
    rm -rf "$projcet_reousrce_path/$AppIconsDir"
    mkdir "$projcet_reousrce_path/$AppIconsDir"

    for icon_item in "${icon_array[@]}";
    do
        sips -Z "$icon_item" "$projcet_reousrce_path/$icon_image_name" --out "$projcet_reousrce_path/$AppIconsDir"/AppIcon_"$icon_item"x"$icon_item".png
    done

    plist_path="${project_path}/${project_name}/Info.plist"
    pbxproj_path="${project_path}/${project_name}.xcodeproj/project.pbxproj"

    sed -i '' "/CFBundleDisplayName/{n;s/<string>.*<\/string>/<string>$currentAppName<\/string>/;}" $plist_path
    sed -i '' "/CFBundleName/{n;s/<string>.*<\/string>/<string>$currentAppName<\/string>/;}" $plist_path
    sed -i '' "/CFBundleIdentifier/{n;s/<string>.*<\/string>/<string>$bidPrefix$currentAppId<\/string>/;}" $plist_path
    sed -i '' "s/PRODUCT_BUNDLE_IDENTIFIER = .*/PRODUCT_BUNDLE_IDENTIFIER = $bidPrefix$currentAppId;/g" $pbxproj_path

    for icon_item in "${icon_array[@]}";
    do
        icon_name = AppIcon_"$icon_item"x"$icon_item".png
        cp "${projcet_reousrce_path}/${AppIconsDir}/${icon_name}" "${project_path}/${project_name}/Assets.xcassets/AppIcon.appiconset/${icon_name}"
    done

    change_name_index=0
    while [[ change_name_index -lt ${#changeNames[@]} ]];
    do
        changeName=${changeNames[change_name_index]}
        changeNameInProj=${changeNamesInProj[change_name_index]}
        let change_name_index++
        #替换app内用到的图标 和 首页那个图
        cp -r "${projcet_reousrce_path}/Others/${changeName}" "${project_path}/${project_name}/${changeNameInProj}"
    done
}

package() {
    rm "$archive_path/$currentAppName.xcworkspace"
    rm "$build_temp_path"
    xcodebuild archive \
    -workspace "$project_path/$project_name.xcworkspace" \
    -scheme "$project_name" \
    -configuration "$MWConfiguration" \
    -archivePath "$archive_path/$currentAppName" \
    clean \
    build \
    -derivedDataPath "$build_temp_path"

    xcodebuild -exportArchive -exportOptionsPlist "$export_plist_path" -archivePath "$archive_path/$currentAppName.xcarchive" -exportPath $output_path/$currentAppId
}

run() {
    sed -i '' "/teamID/{n;s/<string>.*<\/string>/<string>$team_id<\/string>/;}" $export_plist_path
    
    project_index=0
    while [[ project_index -lt ${#appNames[@]} ]];
    do
        currentAppName=${appNames[project_index]}
        echo "$project_index : $currentAppName"
        let project_index++
    done
    echo "999 : Package All"
    echo "Enter index for package...."
    read -p "" package_index

    if [[ $package_index -eq 999 ]]; then
        appNames_new=(${appNames[*]})
        appIds_new=(${appIds[*]})
    else 
        appNames_new=(${appNames[package_index]})
        appIds_new=(${appIds[package_index]})
    fi

    project_index=0
    while [[ project_index -lt ${#appIds_new[@]} ]]; do
        currentAppName=${appNames_new[project_index]}
        currentAppId=${appIds_new[project_index]}
        echo "current package: $currentAppName"
        prepare
        package
        let project_index++
    done
}

run