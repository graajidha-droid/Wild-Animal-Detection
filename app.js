body {
    background-color: rgb(40, 40, 40);
    padding: 10px;
}

.container {
    display: flexbox;
    flex-direction: row;
    padding-top: 20px;
}

.container .left {
    flex: 1;
}

.container .right {
    flex: 1;
}

.context {
    display: flex;
    flex-direction: column;
    padding-left: 50px;
}

.context .top {
    flex: 1;
}

.context .bottom {
    flex: 1;
}


h1 {
    text-align: center;
    font-style: normal;
    font-weight: bolder;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    background-color: rgb(76, 123, 123);
}

h2 {
    font-style: oblique;
    font-weight: bold;
    color: rgb(90, 155, 133);
}

.video {
    border: solid rgb(74, 138, 93);
    border-radius: 8px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.8), 0 6px 20px 0 rgba(0, 0, 0, 0.8);
    display: block;
    width: 50%;
    height: fit-content;
    float: left;
}

#msg {
    font-size: 45px;
    color: #058da4;
    font-style: bold;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}

#anm {
    color: rgb(141, 134, 39);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: medium;
    font-weight: bold;
}

@media only screen and (max-width: 600px) {

    .video{
        width: 100%;
    }

    h1{
        font-size: large;
    }

    #msg{
        font-size: 30px;
        font-family: 'Times New Roman', Times, serif;
    }

    .context {
        padding-left: 10px;
    }
}