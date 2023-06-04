## Github Action Workflow

```yaml
name: ios Deployment

on:
  push:
  	branches:
  		- main
  		- develop

jobs:
	build:
	name: Deploy to TestFlight
	runs-on: macOS-latest
	
	steps:
		- name: Checkout code
		 uses: actions/checkout@v3
		 
		- name: Use Node.js 14
			uses: actions/setup-node@v3
			with:
				node-version: 14.x
				
		- name: Setup xcode
		  uses: maxim-lobanov/setup-xcode@v1
      with:
        xcode-version: latest
        
    - name: Set up NPM authentication
      env:
        NPM_AUTH_TOKEN: ${{ secrets.NPM_AUTH_TOKEN }}
      run: echo "//npm.pkg.github.com/:_authToken=$NPM_AUTH_TOKEN" >> ~/.npmrc
        
    - name: Install Node modules
      run: yarn install --frozen-lockfile
      
    - name: Update and Commit and Push Version Update
      if: ${{ !contains(github.event.head_commit.message, 'version') }}	# 可以添加if条件判断语句
      run: |
        yarn bump --type patch
        git config --global user.name "${{ secrets.GIT_USER_NAME }}"
        git config --global user.email "${{ secrets.GIT_USER_EMAIL }}"
        git add package.json
        git commit -m "Bump version in workflow" --no-verify
        git push
        
      - name: Install Pods
        run: cd ios && pod install && cd ..

      - name: Build IOS App
        uses: yukiarrr/ios-build-action@v1.4.0
        with:
          project-path: 'ios/PROJ.xcodeproj'
          p12-base64: ${{ secrets.IOS_P12_BASE64 }}
          mobileprovision-base64: ${{ secrets.IOS_MOBILE_PROVISION_BASE64 }}
          code-signing-identity: 'Apple Distribution'
          team-id: ${{ secrets.IOS_TEAM_ID }}
          workspace-path: 'ios/PROJ.xcworkspace'
          scheme: proj

      - name: 'Upload app to TestFlight'
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: 'output.ipa'
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_API_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_API_PRIVATE_KEY }}
```

