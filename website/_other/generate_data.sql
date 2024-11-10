-- Insertar usuarios con sus datos de perfil y biografía
INSERT INTO user (email, password, first_name, username, profile_picture, background_image, bio, date_joined)
VALUES
('user1@example.com', 'password1', 'John Doe', 'john_doe', 'https://randomuser.me/api/portraits/men/1.jpg', 'https://randomuser.me/api/portraits/men/1.jpg', 'Software engineer. Passionate about technology and travel.', '2023-01-01 10:00:00'),
('user2@example.com', 'password2', 'Jane Smith', 'jane_smith', 'https://randomuser.me/api/portraits/women/2.jpg', 'https://randomuser.me/api/portraits/women/2.jpg', 'Graphic designer and artist. Love working on creative projects.', '2023-01-02 11:00:00'),
('user3@example.com', 'password3', 'Alice Brown', 'alice_brown', 'https://randomuser.me/api/portraits/women/3.jpg', 'https://randomuser.me/api/portraits/women/3.jpg', 'Marketing expert with a focus on digital marketing strategies.', '2023-01-03 12:00:00'),
('user4@example.com', 'password4', 'Bob White', 'bob_white', 'https://randomuser.me/api/portraits/men/4.jpg', 'https://randomuser.me/api/portraits/men/4.jpg', 'Tech enthusiast. Love coding and playing video games.', '2023-01-04 13:00:00'),
('user5@example.com', 'password5', 'Charlie Green', 'charlie_green', 'https://randomuser.me/api/portraits/men/5.jpg', 'https://randomuser.me/api/portraits/men/5.jpg', 'Professional photographer with a passion for nature.', '2023-01-05 14:00:00'),
('user6@example.com', 'password6', 'Debbie Black', 'debbie_black', 'https://randomuser.me/api/portraits/women/6.jpg', 'https://randomuser.me/api/portraits/women/6.jpg', 'Food critic and writer, exploring the world through food.', '2023-01-06 15:00:00'),
('user7@example.com', 'password7', 'Eve White', 'eve_white', 'https://randomuser.me/api/portraits/women/7.jpg', 'https://randomuser.me/api/portraits/women/7.jpg', 'Entrepreneur and business consultant.', '2023-01-07 16:00:00'),
('user8@example.com', 'password8', 'Frank Black', 'frank_black', 'https://randomuser.me/api/portraits/men/8.jpg', 'https://randomuser.me/api/portraits/men/8.jpg', 'Digital artist, interested in virtual reality and 3D modeling.', '2023-01-08 17:00:00'),
('user9@example.com', 'password9', 'Grace Blue', 'grace_blue', 'https://randomuser.me/api/portraits/women/9.jpg', 'https://randomuser.me/api/portraits/women/9.jpg', 'Public relations specialist. Love networking and creating connections.', '2023-01-09 18:00:00'),
('user10@example.com', 'password10', 'Henry Orange', 'henry_orange', 'https://randomuser.me/api/portraits/men/10.jpg', 'https://randomuser.me/api/portraits/men/10.jpg', 'Engineer with a passion for sustainable technology.', '2023-01-10 19:00:00'),
('user11@example.com', 'password11', 'Isabel Brown', 'isabel_brown', 'https://randomuser.me/api/portraits/women/11.jpg', 'https://randomuser.me/api/portraits/women/11.jpg', 'Interior designer. Specializing in minimalist and modern designs.', '2023-01-11 20:00:00'),
('user12@example.com', 'password12', 'Jack Green', 'jack_green', 'https://randomuser.me/api/portraits/men/12.jpg', 'https://randomuser.me/api/portraits/men/12.jpg', 'Web developer and open-source enthusiast.', '2023-01-12 21:00:00'),
('user13@example.com', 'password13', 'Karen Yellow', 'karen_yellow', 'https://randomuser.me/api/portraits/women/13.jpg', 'https://randomuser.me/api/portraits/women/13.jpg', 'Social media strategist. Helping brands grow their online presence.', '2023-01-13 22:00:00'),
('user14@example.com', 'password14', 'Leo Red', 'leo_red', 'https://randomuser.me/api/portraits/men/14.jpg', 'https://randomuser.me/api/portraits/men/14.jpg', 'Freelance writer and content creator.', '2023-01-14 23:00:00'),
('user15@example.com', 'password15', 'Mia Violet', 'mia_violet', 'https://randomuser.me/api/portraits/women/15.jpg', 'https://randomuser.me/api/portraits/women/15.jpg', 'Photographer specializing in weddings and events.', '2023-01-15 00:00:00'),
('user16@example.com', 'password16', 'Nathan White', 'nathan_white', 'https://randomuser.me/api/portraits/men/16.jpg', 'https://randomuser.me/api/portraits/men/16.jpg', 'Entrepreneur and startup mentor.', '2023-01-16 01:00:00'),
('user17@example.com', 'password17', 'Olivia Blue', 'olivia_blue', 'https://randomuser.me/api/portraits/women/17.jpg', 'https://randomuser.me/api/portraits/women/17.jpg', 'Travel blogger and content creator.', '2023-01-17 02:00:00'),
('user18@example.com', 'password18', 'Paul Grey', 'paul_grey', 'https://randomuser.me/api/portraits/men/18.jpg', 'https://randomuser.me/api/portraits/men/18.jpg', 'Business consultant focused on startups and innovation.', '2023-01-18 03:00:00'),
('user19@example.com', 'password19', 'Quinn Red', 'quinn_red', 'https://randomuser.me/api/portraits/men/19.jpg', 'https://randomuser.me/api/portraits/men/19.jpg', 'Software developer and tech enthusiast.', '2023-01-19 04:00:00'),
('user20@example.com', 'password20', 'Rachel Yellow', 'rachel_yellow', 'https://randomuser.me/api/portraits/women/20.jpg', 'https://randomuser.me/api/portraits/women/20.jpg', 'Fitness trainer and wellness coach.', '2023-01-20 05:00:00');



-- Insertar publicaciones con imágenes o videos
INSERT INTO post (user_id, content, media_url, media_type, post_date)
VALUES
(1, 'Exploring new tech trends!', 'https://example.com/images/tech_trends.jpg', 'image', '2023-02-01 10:00:00'),
(2, 'Just finished a new design project!', 'https://example.com/images/design_project.png', 'image', '2023-02-02 11:00:00'),
(3, 'Launching a new marketing campaign this week!', 'https://example.com/videos/campaign_launch.mp4', 'video', '2023-02-03 12:00:00'),
(4, 'Excited to share my latest tech article!', 'https://example.com/images/tech_article.jpg', 'image', '2023-02-04 13:00:00'),
(5, 'New photography session completed. Check out my work!', 'https://example.com/images/photo_session.jpg', 'image', '2023-02-05 14:00:00'),
(6, 'Tasting new gourmet dishes, check my latest review!', 'https://example.com/images/gourmet_food.jpg', 'image', '2023-02-06 15:00:00'),
(7, 'Great results from our latest consulting project!', 'https://example.com/videos/consulting_project.mp4', 'video', '2023-02-07 16:00:00'),
(8, 'Creating my first virtual reality experience, stay tuned!', 'https://example.com/videos/vr_experience.mp4', 'video', '2023-02-08 17:00:00'),
(9, 'Public relations campaign went live today!', 'https://example.com/images/pr_campaign.jpg', 'image', '2023-02-09 18:00:00'),
(10, 'Sustainable energy solutions for a better future!', 'https://example.com/images/sustainable_energy.jpg', 'image', '2023-02-10 19:00:00'),
(11, 'Loving my new interior design project! Here’s a sneak peek.', 'https://example.com/images/interior_design.jpg', 'image', '2023-02-11 20:00:00'),
(12, 'Just launched a new website for a client. Check it out!', 'https://example.com/images/website_launch.jpg', 'image', '2023-02-12 21:00:00'),
(13, 'Excited about the future of digital marketing.', 'https://example.com/images/digital_marketing.jpg', 'image', '2023-02-13 22:00:00'),
(14, 'My latest article on freelancing, now live!', 'https://example.com/images/freelance_article.jpg', 'image', '2023-02-14 23:00:00'),
(15, 'Captured some amazing moments at the wedding today!', 'https://example.com/images/wedding_photos.jpg', 'image', '2023-02-15 00:00:00'),
(16, 'Great news, we’re expanding the business!', 'https://example.com/images/business_expansion.jpg', 'image', '2023-02-16 01:00:00'),
(17, 'Just visited a new country for my travel blog!', 'https://example.com/images/travel_blog.jpg', 'image', '2023-02-17 02:00:00'),
(18, 'Helping startups grow and innovate, here’s how.', 'https://example.com/images/startups_innovation.jpg', 'image', '2023-02-18 03:00:00'),
(19, 'Diving deep into new coding projects!', 'https://example.com/images/coding_projects.jpg', 'image', '2023-02-19 04:00:00'),
(20, 'Staying fit and healthy with my new workout routine!', 'https://example.com/images/workout_routine.jpg', 'image', '2023-02-20 05:00:00');



-- Insertar comentarios para publicaciones
INSERT INTO comment (user_id, post_id, content, comment_date)
VALUES
(1, 2, 'Great work on this project!', '2023-02-02 12:00:00'),
(2, 3, 'Excited to see your campaign!', '2023-02-03 13:00:00'),
(3, 4, 'Looking forward to reading your article!', '2023-02-04 14:00:00'),
(4, 5, 'Amazing photography, keep it up!', '2023-02-05 15:00:00'),
(5, 6, 'I can’t wait to try this food!', '2023-02-06 16:00:00'),
(6, 7, 'Congrats on the project results!', '2023-02-07 17:00:00'),
(7, 8, 'Virtual reality is the future!', '2023-02-08 18:00:00'),
(8, 9, 'PR campaigns are always exciting!', '2023-02-09 19:00:00'),
(9, 10, 'Sustainable energy is the way forward.', '2023-02-10 20:00:00'),
(10, 11, 'Your interior design is stunning!', '2023-02-11 21:00:00');

-- Insertar relaciones de seguidores
INSERT INTO followers (user_id, follower_id)
VALUES
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 6),
(6, 7),
(7, 8),
(8, 9),
(9, 10),
(10, 11),
(11, 12),
(12, 13),
(13, 14),
(14, 15),
(15, 16),
(16, 17),
(17, 18),
(18, 19),
(19, 20),
(20, 1);


-- Insertar mensajes privados entre usuarios
INSERT INTO private_message (sender_id, receiver_id, message_content, message_date)
VALUES
(1, 2, 'Hey, I really enjoyed your latest design project!', '2023-02-02 12:00:00'),
(2, 3, 'Looking forward to collaborating on your marketing campaign.', '2023-02-03 13:00:00'),
(3, 4, 'Can you share some tips on digital marketing?', '2023-02-04 14:00:00'),
(4, 5, 'I love your photography work, any tips for beginners?', '2023-02-05 15:00:00'),
(5, 6, 'Your food reviews are so interesting! I need new ideas.', '2023-02-06 16:00:00');
