function Run {
    docker run -it -v $($pwd.Path + ":/home") -w /home nathanmurray/idsb
}

function Build {
    docker build -t nathanmurray/idsb .
}