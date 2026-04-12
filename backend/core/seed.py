from datetime import date, datetime, timedelta

from .extensions import db
from ..models import CandidateProfile, Category, Company, CvTemplate, JobPosting, Resume, Tag, User
from .security import hash_password, slugify

DEFAULT_PASSWORD = hash_password("123456")


def seed_initial_data():
    admin = _ensure_user(
        email="myappweb145@gmail.com",
        full_name="System Admin",
        role="admin",
        auth_method_preference="password",
    )
    recruiter = _ensure_user(
        email="2251012132tien@ou.edu.vn",
        full_name="Tien Recruiter",
        role="recruiter",
        auth_method_preference="otp",
    )
    candidate = _ensure_user(
        email="dinhtien09102004@gmail.com",
        full_name="Tien Candidate",
        role="candidate",
        auth_method_preference="otp",
    )

    company = _ensure_company(
        recruiter_user=recruiter,
        company_name="MyApp Web Recruitment",
        tax_code="0101234567",
        website="https://myappweb.example.com",
        address="TP. Hồ Chí Minh",
        description="Công ty chuyên tuyển dụng và phát triển hệ thống web việc làm.",
        industry="Công nghệ thông tin",
        logo_url="https://res.cloudinary.com/dqukehyry/image/upload/v1775390271/creative-modern-letter-u-logo-600nw-2657043749_xiqk4d.jpg",
    )

    if not CandidateProfile.query.filter_by(user_id=candidate.id).first():
        db.session.add(
            CandidateProfile(
                user_id=candidate.id,
                dob=date(2004, 10, 9),
                gender="male",
                address="TP. Hồ Chí Minh",
                headline="Frontend / Python Developer",
                summary="Ứng viên có nền tảng React, Flask, MySQL và thiết kế giao diện web.",
                current_title="Sinh viên IT",
                years_experience=2,
                expected_salary="12-18 triệu",
                desired_location="TP. Hồ Chí Minh",
                education="Đại học Open University",
                experience="Đã làm đồ án hệ thống tuyển dụng online.",
            )
        )

    categories = {}
    for name, slug, description in [
        ("Ngành nghề", "industry", "Nhóm lĩnh vực/ngành nghề"),
        ("Kỹ năng", "skill", "Nhóm kỹ năng chuyên môn"),
        ("Kinh nghiệm", "experience", "Nhóm cấp độ kinh nghiệm"),
        ("Địa điểm", "location", "Nhóm địa điểm làm việc"),
        ("Hình thức", "job_type", "Nhóm loại việc làm"),
    ]:
        category = _ensure_category(name=name, slug=slug, description=description)
        categories[slug] = category

    tags = {}
    for name, category_slug, description in [
        ("React", "skill", "Kỹ năng React"),
        ("Python", "skill", "Kỹ năng Python"),
        ("Flask", "skill", "Kỹ năng Flask"),
        ("MySQL", "skill", "Kỹ năng MySQL"),
        ("HTML/CSS", "skill", "Kỹ năng giao diện web"),
        ("IT", "industry", "Lĩnh vực công nghệ thông tin"),
        ("Frontend", "industry", "Lĩnh vực frontend"),
        ("Backend", "industry", "Lĩnh vực backend"),
        ("UI/UX", "industry", "Thiết kế giao diện và trải nghiệm"),
        ("Data", "industry", "Phân tích dữ liệu"),
        ("QA", "industry", "Kiểm thử phần mềm"),
        ("Sales", "industry", "Kinh doanh và bán hàng"),
        ("Product", "industry", "Quản lý sản phẩm"),
        ("Junior", "experience", "Cấp độ Junior"),
        ("Middle", "experience", "Cấp độ Middle"),
        ("Full-time", "job_type", "Loại công việc toàn thời gian"),
        ("Part-time", "job_type", "Loại công việc bán thời gian"),
        ("TP HCM", "location", "Khu vực TP. Hồ Chí Minh"),
        ("Ha Noi", "location", "Khu vực Hà Nội"),
        ("Da Nang", "location", "Khu vực Đà Nẵng"),
        ("Can Tho", "location", "Khu vực Cần Thơ"),
        ("Remote", "location", "Làm việc từ xa"),
        ("Marketing", "industry", "Lĩnh vực marketing"),
        ("Finance", "industry", "Lĩnh vực tài chính"),
        ("HR", "industry", "Lĩnh vực nhân sự"),
        ("Operations", "industry", "Lĩnh vực vận hành"),
        ("Logistics", "industry", "Lĩnh vực logistics"),
        ("E-commerce", "industry", "Lĩnh vực thương mại điện tử"),
        ("Design", "industry", "Lĩnh vực thiết kế"),
        ("Senior", "experience", "Cấp độ Senior"),
        ("Fresher", "experience", "Cấp độ Fresher"),
        ("Contract", "job_type", "Loại hợp đồng"),
        ("Internship", "job_type", "Loại thực tập"),
        ("JavaScript", "skill", "Kỹ năng JavaScript"),
        ("SQL", "skill", "Kỹ năng SQL"),
        ("Figma", "skill", "Kỹ năng Figma"),
        ("Power BI", "skill", "Kỹ năng Power BI"),
        ("Excel", "skill", "Kỹ năng Excel"),
        ("SEO", "skill", "Kỹ năng SEO"),
        ("Communication", "skill", "Kỹ năng giao tiếp"),
        ("Node.js", "skill", "Kỹ năng Node.js"),
        ("Digital Marketing", "skill", "Kỹ năng marketing số"),
    ]:
        tag = _ensure_tag(name=name, category=categories[category_slug], description=description)
        tags[slugify(name)] = tag

    job_1 = _ensure_job(
        slug="python-flask-developer",
        recruiter=recruiter,
        company=company,
        title="Python Flask Developer",
        summary="Phát triển hệ thống tuyển dụng web.",
        description="Xây dựng backend Flask REST API cho hệ thống cổng thông tin việc làm.",
        requirements="Biết Flask, SQLAlchemy, MySQL, REST API, Git.",
        responsibilities="Phát triển API, tối ưu database, làm việc với frontend React.",
        location="TP. Hồ Chí Minh",
        workplace_type="hybrid",
        employment_type="full-time",
        experience_level="junior",
        salary_min=15000000,
        salary_max=25000000,
        vacancy_count=2,
        deadline=date.today() + timedelta(days=30),
        is_featured=True,
    )
    job_1.tags = [tags[slugify(name)] for name in ["Python", "Flask", "MySQL", "IT", "Junior", "Full-time", "TP HCM"]]

    job_2 = _ensure_job(
        slug="frontend-react-developer",
        recruiter=recruiter,
        company=company,
        title="Frontend React Developer",
        summary="Thiết kế giao diện và trải nghiệm người dùng.",
        description="Xây dựng giao diện React cho tuyển dụng và CV online.",
        requirements="React, HTML, CSS, JavaScript, responsive UI.",
        responsibilities="Xây dựng màn hình, form, state management.",
        location="Hà Nội",
        workplace_type="remote",
        employment_type="full-time",
        experience_level="middle",
        salary_min=18000000,
        salary_max=30000000,
        vacancy_count=1,
        deadline=date.today() + timedelta(days=45),
    )
    job_2.tags = [tags[slugify(name)] for name in ["React", "Frontend", "Middle", "Full-time", "Ha Noi"]]

    job_3 = _ensure_job(
        slug="ui-ux-designer",
        recruiter=recruiter,
        company=company,
        title="UI/UX Designer",
        summary="Thiết kế giao diện và trải nghiệm cho hệ thống việc làm.",
        description="Tham gia thiết kế flow người dùng, visual system và UI cho candidate/recruiter.",
        requirements="Figma, wireframe, design system, thẩm mỹ tốt.",
        responsibilities="Phối hợp với frontend và product để hoàn thiện trải nghiệm người dùng.",
        location="TP. Hồ Chí Minh",
        workplace_type="hybrid",
        employment_type="full-time",
        experience_level="middle",
        salary_min=14000000,
        salary_max=22000000,
        vacancy_count=1,
        deadline=date.today() + timedelta(days=30),
        is_featured=True,
    )
    job_3.tags = [tags[slugify(name)] for name in ["UI/UX", "React", "Middle", "TP HCM"]]

    job_4 = _ensure_job(
        slug="qa-automation-engineer",
        recruiter=recruiter,
        company=company,
        title="QA Automation Engineer",
        summary="Xây dựng kiểm thử và ổn định hệ thống portal.",
        description="Phát triển automated test case, regression test và quality checks cho web app.",
        requirements="Testing mindset, SQL cơ bản, validate API.",
        responsibilities="Đảm bảo các bản release hoạt động tốt trên web và mobile.",
        location="Remote",
        workplace_type="remote",
        employment_type="full-time",
        experience_level="junior",
        salary_min=10000000,
        salary_max=16000000,
        vacancy_count=1,
        deadline=date.today() + timedelta(days=30),
    )
    job_4.tags = [tags[slugify(name)] for name in ["QA", "MySQL", "Remote", "Junior"]]

    extra_employers = [
        {
            "email": "hr@novacommerce.vn",
            "full_name": "Nova Commerce HR",
            "company_name": "Nova Commerce",
            "tax_code": "0319876543",
            "website": "https://novacommerce.vn",
            "address": "Quận 3, TP. Hồ Chí Minh",
            "description": "Doanh nghiệp thương mại điện tử tập trung vào tăng trưởng và công nghệ.",
            "industry": "E-commerce",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390271/original-ac839f228c8ebe7139e7a9cfcae7d3fa_vgpvbl.png",
            "jobs": [
                {
                    "slug": "ecommerce-backend-engineer",
                    "title": "E-commerce Backend Engineer",
                    "summary": "Xây dựng API cho hệ thống bán hàng đa kênh.",
                    "description": "Phát triển backend cho platform e-commerce, quản lý đơn hàng, thanh toán và tồn kho.",
                    "requirements": "Node.js, SQL, REST API, caching, hệ thống đơn hàng.",
                    "responsibilities": "Tối ưu hiệu năng, bảo đảm luồng checkout và tích hợp dịch vụ third-party.",
                    "location": "TP. Hồ Chí Minh",
                    "workplace_type": "hybrid",
                    "employment_type": "full-time",
                    "experience_level": "middle",
                    "salary_min": 18000000,
                    "salary_max": 30000000,
                    "vacancy_count": 2,
                    "deadline_days": 40,
                    "is_featured": True,
                    "tags": ["Backend", "Node.js", "SQL", "E-commerce", "Middle", "Full-time", "TP HCM"],
                },
                {
                    "slug": "performance-marketing-specialist",
                    "title": "Performance Marketing Specialist",
                    "summary": "Tối ưu quảng cáo và tăng trưởng doanh thu.",
                    "description": "Phụ trách quảng cáo digital, tracking, landing page conversion và báo cáo hiệu quả.",
                    "requirements": "Digital Marketing, SEO, communication, Excel, analytics.",
                    "responsibilities": "Theo dõi ROAS, A/B testing và tối ưu chiến dịch quảng cáo.",
                    "location": "TP. Hồ Chí Minh",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "junior",
                    "salary_min": 12000000,
                    "salary_max": 20000000,
                    "vacancy_count": 1,
                    "deadline_days": 35,
                    "is_featured": False,
                    "tags": ["Marketing", "Digital Marketing", "SEO", "Excel", "Junior", "Full-time", "TP HCM"],
                },
            ],
        },
        {
            "email": "hello@brightstudio.vn",
            "full_name": "Bright Studio HR",
            "company_name": "Bright Studio",
            "tax_code": "0312468024",
            "website": "https://brightstudio.vn",
            "address": "Hà Nội",
            "description": "Studio thiết kế sản phẩm số và giao diện cho web/mobile.",
            "industry": "Design",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390271/business-logo-template-minimal-branding-design-vector_53876-136229_b4ov5l.jpg",
            "jobs": [
                {
                    "slug": "product-designer",
                    "title": "Product Designer",
                    "summary": "Thiết kế sản phẩm số cho nền tảng việc làm.",
                    "description": "Phụ trách user flow, wireframe, UI system và prototype.",
                    "requirements": "Figma, product thinking, UI system, teamwork.",
                    "responsibilities": "Làm việc với frontend, product và recruiter dashboard.",
                    "location": "Hà Nội",
                    "workplace_type": "hybrid",
                    "employment_type": "full-time",
                    "experience_level": "middle",
                    "salary_min": 16000000,
                    "salary_max": 26000000,
                    "vacancy_count": 1,
                    "deadline_days": 30,
                    "is_featured": True,
                    "tags": ["Design", "Figma", "UI/UX", "Product", "Middle", "Full-time", "Ha Noi"],
                }
            ],
        },
        {
            "email": "careers@greenleafhr.vn",
            "full_name": "GreenLeaf HR",
            "company_name": "GreenLeaf HR",
            "tax_code": "0201357901",
            "website": "https://greenleafhr.vn",
            "address": "Đà Nẵng",
            "description": "Đơn vị tuyển dụng và tư vấn nhân sự cho các doanh nghiệp công nghệ.",
            "industry": "HR",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390271/2bfb04ad814c4995f0c537c68db5cd0b-multicolor-swirls-circle-logo_nsrgtn.png",
            "jobs": [
                {
                    "slug": "talent-acquisition-specialist",
                    "title": "Talent Acquisition Specialist",
                    "summary": "Tìm kiếm và sàng lọc ứng viên công nghệ.",
                    "description": "Quản lý nguồn ứng viên, xây dựng quan hệ với candidate và phối hợp hiring manager.",
                    "requirements": "Communication, HR mindset, sourcing, CRM.",
                    "responsibilities": "Đăng tin, phỏng vấn sơ bộ và theo dõi pipeline tuyển dụng.",
                    "location": "Đà Nẵng",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "middle",
                    "salary_min": 13000000,
                    "salary_max": 21000000,
                    "vacancy_count": 1,
                    "deadline_days": 28,
                    "is_featured": False,
                    "tags": ["HR", "Communication", "Middle", "Full-time", "Da Nang"],
                }
            ],
        },
        {
            "email": "jobs@fincore.vn",
            "full_name": "FinCore HR",
            "company_name": "FinCore Analytics",
            "tax_code": "0109988776",
            "website": "https://fincore.vn",
            "address": "Quận 7, TP. Hồ Chí Minh",
            "description": "Công ty phân tích dữ liệu và giải pháp tài chính.",
            "industry": "Finance",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390270/bb19b75c7489d8dadb8b1b709bb8ee65_yoymlk.png",
            "jobs": [
                {
                    "slug": "data-analyst",
                    "title": "Data Analyst",
                    "summary": "Phân tích dữ liệu doanh thu và hành vi người dùng.",
                    "description": "Tổng hợp dashboard, phân tích KPI và hỗ trợ business quyết định.",
                    "requirements": "SQL, Excel, Power BI, tư duy phân tích.",
                    "responsibilities": "Xây dựng báo cáo định kỳ và insight cho quản lý.",
                    "location": "TP. Hồ Chí Minh",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "junior",
                    "salary_min": 14000000,
                    "salary_max": 24000000,
                    "vacancy_count": 2,
                    "deadline_days": 30,
                    "is_featured": True,
                    "tags": ["Data", "SQL", "Excel", "Power BI", "Junior", "Full-time", "TP HCM"],
                },
                {
                    "slug": "bi-engineer",
                    "title": "BI Engineer",
                    "summary": "Xây dựng pipeline và báo cáo BI.",
                    "description": "Phát triển dashboard và mô hình dữ liệu phục vụ báo cáo tài chính.",
                    "requirements": "SQL, Power BI, data modeling, analytics.",
                    "responsibilities": "Tối ưu mô hình dữ liệu và trực quan hóa báo cáo.",
                    "location": "Remote",
                    "workplace_type": "remote",
                    "employment_type": "contract",
                    "experience_level": "middle",
                    "salary_min": 20000000,
                    "salary_max": 32000000,
                    "vacancy_count": 1,
                    "deadline_days": 25,
                    "is_featured": False,
                    "tags": ["Data", "SQL", "Power BI", "Finance", "Middle", "Contract", "Remote"],
                },
            ],
        },
        {
            "email": "careers@atlaslogistics.vn",
            "full_name": "Atlas Logistics HR",
            "company_name": "Atlas Logistics",
            "tax_code": "0311122334",
            "website": "https://atlaslogistics.vn",
            "address": "Cần Thơ",
            "description": "Doanh nghiệp logistics và vận hành chuỗi cung ứng.",
            "industry": "Logistics",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390270/d2c16d99034f9407fd708dfc3356c688_d9prfy.jpg",
            "jobs": [
                {
                    "slug": "fullstack-react-nodejs-developer",
                    "title": "Fullstack React Node.js Developer",
                    "summary": "Xây dựng hệ thống quản lý vận hành và tuyển dụng nội bộ.",
                    "description": "Tham gia phát triển web app cho vận hành nội bộ, báo cáo và quản lý kho.",
                    "requirements": "React, Node.js, SQL, REST API.",
                    "responsibilities": "Xây dựng module quản trị, tối ưu dữ liệu và bảo trì backend.",
                    "location": "Cần Thơ",
                    "workplace_type": "hybrid",
                    "employment_type": "full-time",
                    "experience_level": "middle",
                    "salary_min": 17000000,
                    "salary_max": 28000000,
                    "vacancy_count": 1,
                    "deadline_days": 35,
                    "is_featured": False,
                    "tags": ["Frontend", "Backend", "Node.js", "React", "Middle", "Full-time", "Can Tho"],
                },
                {
                    "slug": "operations-coordinator",
                    "title": "Operations Coordinator",
                    "summary": "Điều phối vận hành và xử lý đơn hàng.",
                    "description": "Phối hợp đội vận hành, theo dõi tiến độ và tối ưu workflow.",
                    "requirements": "Operations, communication, Excel, process thinking.",
                    "responsibilities": "Đảm bảo quy trình vận hành trơn tru và theo dõi KPI.",
                    "location": "Cần Thơ",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "junior",
                    "salary_min": 10000000,
                    "salary_max": 15000000,
                    "vacancy_count": 1,
                    "deadline_days": 20,
                    "is_featured": False,
                    "tags": ["Operations", "Excel", "Communication", "Junior", "Full-time", "Can Tho"],
                },
            ],
        },
        {
            "email": "jobs@eduspark.vn",
            "full_name": "EduSpark HR",
            "company_name": "EduSpark",
            "tax_code": "0405566778",
            "website": "https://eduspark.vn",
            "address": "Hà Nội",
            "description": "Nền tảng giáo dục số và học tập trực tuyến.",
            "industry": "Education",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390270/0c61fa6a79a7055a4dfd9b288e882c41_zrgmxv.jpg",
            "jobs": [
                {
                    "slug": "frontend-engineer-education",
                    "title": "Frontend Engineer",
                    "summary": "Phát triển giao diện học tập trực tuyến.",
                    "description": "Xây dựng web app cho học viên, giảng viên và admin dashboard.",
                    "requirements": "React, HTML/CSS, JavaScript, UX mindset.",
                    "responsibilities": "Tối ưu UI, cải thiện trải nghiệm học và tracking tiến độ.",
                    "location": "Hà Nội",
                    "workplace_type": "hybrid",
                    "employment_type": "full-time",
                    "experience_level": "junior",
                    "salary_min": 15000000,
                    "salary_max": 23000000,
                    "vacancy_count": 1,
                    "deadline_days": 28,
                    "is_featured": True,
                    "tags": ["Frontend", "React", "JavaScript", "HTML/CSS", "Junior", "Full-time", "Ha Noi"],
                }
            ],
        },
        {
            "email": "sales@salespulse.vn",
            "full_name": "SalesPulse HR",
            "company_name": "SalesPulse",
            "tax_code": "0508899001",
            "website": "https://salespulse.vn",
            "address": "TP. Hồ Chí Minh",
            "description": "Đội ngũ bán hàng và tăng trưởng doanh số cho sản phẩm số.",
            "industry": "Sales",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390269/291-logo-1711991296.916_iqxlt2.svg",
            "jobs": [
                {
                    "slug": "digital-marketing-executive",
                    "title": "Digital Marketing Executive",
                    "summary": "Quản lý chiến dịch digital và nội dung quảng bá.",
                    "description": "Lập kế hoạch marketing, tối ưu nội dung và theo dõi hiệu quả chiến dịch.",
                    "requirements": "Digital Marketing, SEO, communication, content.",
                    "responsibilities": "Chạy chiến dịch, đo lường KPI và phối hợp sales.",
                    "location": "TP. Hồ Chí Minh",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "middle",
                    "salary_min": 13000000,
                    "salary_max": 21000000,
                    "vacancy_count": 1,
                    "deadline_days": 22,
                    "is_featured": False,
                    "tags": ["Marketing", "Digital Marketing", "SEO", "Communication", "Middle", "Full-time", "TP HCM"],
                },
                {
                    "slug": "account-executive",
                    "title": "Account Executive",
                    "summary": "Tư vấn và chăm sóc khách hàng doanh nghiệp.",
                    "description": "Làm việc với khách hàng, hiểu nhu cầu và đề xuất giải pháp phù hợp.",
                    "requirements": "Sales, communication, CRM, tư duy dịch vụ.",
                    "responsibilities": "Quản lý pipeline khách hàng và chăm sóc sau bán hàng.",
                    "location": "TP. Hồ Chí Minh",
                    "workplace_type": "onsite",
                    "employment_type": "full-time",
                    "experience_level": "junior",
                    "salary_min": 11000000,
                    "salary_max": 18000000,
                    "vacancy_count": 2,
                    "deadline_days": 22,
                    "is_featured": False,
                    "tags": ["Sales", "Communication", "Junior", "Full-time", "TP HCM"],
                },
            ],
        },
        {
            "email": "careers@cloudops.asia",
            "full_name": "CloudOps Asia",
            "company_name": "CloudOps Asia",
            "tax_code": "0603344556",
            "website": "https://cloudops.asia",
            "address": "Đà Nẵng",
            "description": "Doanh nghiệp hạ tầng cloud và vận hành hệ thống.",
            "industry": "Operations",
            "logo_url": "https://res.cloudinary.com/dqukehyry/image/upload/v1775390271/original-ac839f228c8ebe7139e7a9cfcae7d3fa_vgpvbl.png",
            "jobs": [
                {
                    "slug": "devops-engineer",
                    "title": "DevOps Engineer",
                    "summary": "Triển khai hạ tầng và tối ưu CI/CD.",
                    "description": "Xây dựng pipeline, quản lý container và giám sát hệ thống production.",
                    "requirements": "Linux, Docker, CI/CD, cloud, automation.",
                    "responsibilities": "Đảm bảo uptime và hỗ trợ triển khai release an toàn.",
                    "location": "Đà Nẵng",
                    "workplace_type": "remote",
                    "employment_type": "full-time",
                    "experience_level": "senior",
                    "salary_min": 25000000,
                    "salary_max": 40000000,
                    "vacancy_count": 1,
                    "deadline_days": 30,
                    "is_featured": True,
                    "tags": ["Backend", "Operations", "Senior", "Full-time", "Da Nang", "Remote"],
                }
            ],
        },
    ]

    for item in extra_employers:
        recruiter_user = _ensure_user(
            email=item["email"],
            full_name=item["full_name"],
            role="recruiter",
            auth_method_preference="otp",
        )
        extra_company = _ensure_company(
            recruiter_user=recruiter_user,
            company_name=item["company_name"],
            tax_code=item["tax_code"],
            website=item["website"],
            address=item["address"],
            description=item["description"],
            logo_url=item["logo_url"],
            industry=item["industry"],
        )
        for job_data in item["jobs"]:
            job = _ensure_job(
                slug=job_data["slug"],
                recruiter=recruiter_user,
                company=extra_company,
                title=job_data["title"],
                summary=job_data["summary"],
                description=job_data["description"],
                requirements=job_data["requirements"],
                responsibilities=job_data["responsibilities"],
                location=job_data["location"],
                workplace_type=job_data["workplace_type"],
                employment_type=job_data["employment_type"],
                experience_level=job_data["experience_level"],
                salary_min=job_data["salary_min"],
                salary_max=job_data["salary_max"],
                salary_currency="VND",
                vacancy_count=job_data["vacancy_count"],
                deadline=date.today() + timedelta(days=job_data["deadline_days"]),
                is_featured=job_data["is_featured"],
            )
            job.tags = [tags[slugify(name)] for name in job_data["tags"]]

    preview_urls = {
        "modern-blue": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393343/nguyen-thi-truc-mai_4010758_561084a9cd7112f2_4010758_orgnyz.pdf",
        "ats-clean": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393343/nguyen-thi-truc-mai_4010756_Joboko_4fd074991dc96370_4010756_rgglu9.pdf",
        "creative-minimal": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393344/nguyen-thi-truc-mai_4010752_Joboko_84c60ffaca3a6456_4010752_ag2sng.pdf",
        "product-designer": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393344/nguyen-thi-truc-mai_4010753_Joboko_881080294f84b32f_4010753_ptymya.pdf",
        "data-analyst": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393344/nguyen-thi-truc-mai_4010748_Joboko_8250e56278eb8bea_4010748_g1muvd.pdf",
        "hr-executive": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393344/nguyen-thi-truc-mai_4010751_Joboko_b88f4eb6aec594f1_4010751_enmjel.pdf",
        "marketing-pro": "https://res.cloudinary.com/dqukehyry/image/upload/v1775393345/tien-dinh-bich_4010744_Joboko_cab46210c308a2a6_4010744_gbarcg.pdf",
    }
    for name, slug_value, summary in [
        ("Modern Blue", "modern-blue", "Mẫu CV hiện đại cho ứng viên công nghệ"),
        ("ATS Clean", "ats-clean", "Thiết kế tối giản tối ưu cho hệ thống ATS"),
        ("Creative Minimal", "creative-minimal", "Mẫu CV sáng tạo cho thiết kế và marketing"),
        ("Product Designer", "product-designer", "Phù hợp cho UI/UX và product designer"),
        ("Data Analyst", "data-analyst", "Tập trung vào dữ liệu, bảng biểu và KPI"),
        ("HR Executive", "hr-executive", "Mẫu CV cho nhân sự và tuyển dụng"),
        ("Marketing Pro", "marketing-pro", "Mẫu CV cho digital marketing và content"),
    ]:
        _ensure_cv_template(
            name=name,
            slug=slugify(slug_value),
            summary=summary,
            description=summary,
            thumbnail_url=None,
            preview_url=preview_urls.get(slugify(slug_value)),
            file_format="both",
        )

    if not Resume.query.filter_by(title="CV mẫu online", user_id=candidate.id).first():
        resume = Resume(
            user_id=candidate.id,
            title="CV mẫu online",
            source_type="manual",
            template_name="Modern Blue",
            raw_text="React Python Flask MySQL HTML CSS JavaScript",
            structured_json={"desired_location": "TP. Hồ Chí Minh", "years_experience": 2},
            is_primary=True,
        )
        resume.tags = [tags[slugify(name)] for name in ["React", "Python", "Flask", "MySQL", "IT", "Junior", "TP HCM"]]
        db.session.add(resume)

    db.session.commit()


def _ensure_user(email: str, full_name: str, role: str, auth_method_preference: str) -> User:
    user = User.query.filter_by(email=email).first()
    if user:
        user.full_name = full_name
        user.role = role
        user.auth_method_preference = auth_method_preference
        user.status = "active"
        user.email_verified = True
        if not user.password_hash:
            user.password_hash = DEFAULT_PASSWORD
        return user

    user = User(
        full_name=full_name,
        email=email,
        password_hash=DEFAULT_PASSWORD,
        role=role,
        email_verified=True,
        status="active",
        auth_method_preference=auth_method_preference,
    )
    db.session.add(user)
    db.session.flush()
    return user


def _ensure_category(name: str, slug: str, description: str) -> Category:
    category = Category.query.filter_by(slug=slug).first()
    if category:
        category.name = name
        category.description = description
        category.is_active = True
        return category

    category = Category(name=name, slug=slug, description=description, is_active=True)
    db.session.add(category)
    db.session.flush()
    return category


def _ensure_tag(name: str, category: Category, description: str) -> Tag:
    slug = slugify(name)
    tag = Tag.query.filter((Tag.slug == slug) | (Tag.name == name)).first()
    if tag:
        tag.name = name
        tag.slug = slug
        tag.category = category
        tag.description = description
        tag.is_active = True
        return tag

    tag = Tag(name=name, slug=slug, category=category, description=description, is_active=True)
    db.session.add(tag)
    db.session.flush()
    return tag


def _ensure_job(slug: str, recruiter: User, company: Company, **fields) -> JobPosting:
    job = JobPosting.query.filter_by(slug=slug).first()
    if job:
        for key, value in fields.items():
            setattr(job, key, value)
        if job.status == "published" and not job.published_at:
            job.published_at = datetime.utcnow()
        return job

    job = JobPosting(
        recruiter_user_id=recruiter.id,
        company_id=company.id,
        slug=slug,
        status="published",
        published_at=datetime.utcnow(),
        **fields,
    )
    db.session.add(job)
    db.session.flush()
    return job


def _ensure_company(
    recruiter_user: User,
    company_name: str,
    tax_code: str,
    website: str,
    address: str,
    description: str,
    logo_url: str,
    industry: str,
) -> Company:
    company = Company.query.filter_by(recruiter_user_id=recruiter_user.id).first()
    if company:
        company.company_name = company_name
        company.tax_code = tax_code
        company.website = website
        company.address = address
        company.description = description
        company.logo_url = logo_url
        company.industry = industry
        return company

    company = Company(
        recruiter_user_id=recruiter_user.id,
        company_name=company_name,
        tax_code=tax_code,
        website=website,
        address=address,
        description=description,
        logo_url=logo_url,
        industry=industry,
    )
    db.session.add(company)
    db.session.flush()
    return company


def _ensure_cv_template(
    name: str,
    slug: str,
    summary: str,
    description: str,
    thumbnail_url: str | None,
    preview_url: str | None,
    file_format: str,
) -> CvTemplate:
    template = CvTemplate.query.filter_by(slug=slug).first()
    if template:
        template.name = name
        template.summary = summary
        template.description = description
        template.thumbnail_url = thumbnail_url
        template.preview_url = preview_url
        template.file_format = file_format
        template.is_active = True
        return template

    template = CvTemplate(
        name=name,
        slug=slug,
        summary=summary,
        description=description,
        thumbnail_url=thumbnail_url,
        preview_url=preview_url,
        file_format=file_format,
        is_active=True,
    )
    db.session.add(template)
    db.session.flush()
    return template