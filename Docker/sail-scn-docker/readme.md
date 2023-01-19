# build command
docker build -f df_scn --build-arg git_personal_token={git_personal_token} --build-arg branch_datascience={branch_datascience} --build-arg branch_datascience={branch_engineering} -t sail/scn .

# running the scn
docker run im_scn -p 5010:5010

# running the agregator
