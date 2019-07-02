DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS secret;

CREATE TABLE article (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL
);

INSERT INTO article (title, content, created_at)
    VALUES ('Yandex Debuts Smart Home Ecosystem Powered by Intelligent Assistant, Alice',
            'Yandex, a technology company that builds intelligent products and ' ||
            'services powered by machine learning, unveiled Russia’s first smart home ecosystem ' ||
            'powered by the company’s intelligent assistant, Alice.  Alice can now turn on lights, ' ||
            'adjust a thermostat, control a TV, or even make coffee.  Leading manufacturers such ' ||
            'as Philips, Xiaomi, Samsung, and Redmond will offer Yandex smart home compatible products, ' ||
            'including smart bulbs, plugs, and appliances.',
            '2019-05-23 10:00:00');

INSERT INTO article (title, content, created_at)
    VALUES ('Yandex Launches Personalized Streaming Channel and an HDMI Dongle Media Player',
            'Yandex, a technology company that builds intelligent products and services powered by machine ' ||
            'learning, now provides users with a personalized video stream for live and on-demand video on ' ||
            'the company’s streaming content platform, Yandex.Live. Today Yandex also announced the launch ' ||
            'of a new HDMI dongle, Yandex.Module, to enable users to stream Yandex.Live to their TV screens.',
            '2019-05-23 09:15:00');

INSERT INTO article (title, content, created_at)
    VALUES ('Yandex Launches Public Cloud Platform Yandex.Cloud',
            'Yandex has launched its intelligent public cloud platform,Yandex.Cloud, enabling companies to ' ||
            'develop and support web apps and services using Yandex’s advanced technologies and infrastructure. ' ||
            'Yandex.Cloud is deployed across local data centers, enabling companies to store and use databases ' ||
            'containing personal data in Russia as required by law.',
            '2018-09-05 15:12:00');

CREATE TABLE secret (
    content VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO secret (content) VALUES ('TOP SECRET');