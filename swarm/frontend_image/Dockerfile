# pull the base image
FROM patrickeholland/frontend_packages_installed

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# add app
COPY ./app ./app
