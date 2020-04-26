FROM nginx:1.16
LABEL MAINTAINER="Hadi Khani | https://danadev.ir"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]