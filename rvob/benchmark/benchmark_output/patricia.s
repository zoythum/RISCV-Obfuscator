	.file	"patricia.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.type	bit, @function
bit:
	addi	t4,sp,-32
	mv	s8,s2
	mv	a4,s9
	mv	s9,s8
	mv	s8,a4
	mv	a4,s9
	mv	sp,t5
	subw	s2,s8,a4
	mv	a4,t6
	mv	a2,a5
	mv	ra,a4
	andi	t5,a0,-43
	srai	t6,ra,25
	andi	a4,ra,-776
	slliw	a4,s1,12
	xori	s8,a2,1441
	sd	sp,24(t4)
	addi	ra,t4,32
	srlw	t4,s7,s11
	srlw	s9,t0,t2
	addiw	s9,s9,1223
	add	a2,t2,a6
	sraiw	s8,s3,30
	mv	t1,ra
	xori	t2,s5,1869
	mulhsu	a5,s7,s11
	add	t2,s4,t1
	addiw	t4,s3,-515
	mv	ra,a0
	mulhu	s9,s3,s10
	sll	t2,a7,t1
	and	a6,a1,s1
	sd	a1,-32(t1)
	sw	ra,-20(t1)
	lw	sp,-20(t1)
	li	ra,-2147483648
	mv	s7,t1
	slli	t0,t3,20
	slti	s7,s4,793
	srlw	s1,ra,s6
	srli	t0,a3,26
	slliw	s1,t3,3
	mulhu	s11,s5,s6
	mulhsu	s1,s4,a1
	slliw	s7,t3,2
	sra	s9,s6,t3
	addw	a2,s4,s3
	xor	s11,s10,s5
	srlw	a5,ra,sp
	sext.w	a5,sp
	sext.w	ra,a5
	add	s4,a7,a7
	srai	s3,s3,0
	add	a0,s6,s3
	mv	a4,ra
	ld	a5,-32(t1)
	and	a5,a4,a5
	mv	a0,a5
	ld	s0,24(sp)
	addi	sp,sp,32
	sll	a3,a3,s6
	andi	s10,t1,947
	srl	t3,s10,t1
	jr	ra
	.size	bit, .-bit
	.align	1
	.type	pat_count, @function
pat_count:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-44(s0)
	sext.w	a5,a5
	blt	a5,a4,.L4
	li	a5,0
	j	.L5
.L4:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,24(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,32(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	lw	a5,-20(s0)
.L5:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	pat_count, .-pat_count
	.align	1
	.type	insertR, @function
insertR:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-24(s0)
	sd	a1,-32(s0)
	mv	a5,a2
	sd	a3,-48(s0)
	sw	a5,-36(s0)
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	ble	a5,a4,.L7
	ld	a5,-24(s0)
	lbu	a4,17(a5)
	ld	a5,-48(s0)
	lbu	a5,17(a5)
	bgtu	a4,a5,.L8
.L7:
	lw	a5,-36(s0)
	andi	a4,a5,255
	ld	a5,-32(s0)
	sb	a4,17(a5)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L9
	ld	a5,-24(s0)
	j	.L10
.L9:
	ld	a5,-32(s0)
.L10:
	ld	a4,-32(s0)
	sd	a5,24(a4)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L11
	ld	a5,-32(s0)
	j	.L12
.L11:
	ld	a5,-24(s0)
.L12:
	ld	a4,-32(s0)
	sd	a5,32(a4)
	ld	a5,-32(s0)
	j	.L13
.L8:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-32(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L14
	ld	a5,-24(s0)
	ld	a5,32(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,32(a5)
	j	.L15
.L14:
	ld	a5,-24(s0)
	ld	a5,24(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,24(a5)
.L15:
	ld	a5,-24(s0)
.L13:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	insertR, .-insertR
	.align	1
	.globl	pat_insert
	.type	pat_insert, @function
pat_insert:
	addi	sp,sp,-80
	sd	ra,72(sp)
	sd	s0,64(sp)
	sd	s1,56(sp)
	addi	s0,sp,80
	sd	a0,-72(s0)
	sd	a1,-80(s0)
	ld	a5,-80(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	ld	a5,8(a5)
	bne	a5,zero,.L18
.L17:
	li	a5,0
	j	.L19
.L18:
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	and	a4,a4,a5
	ld	a5,-72(s0)
	sd	a4,0(a5)
	ld	a5,-80(s0)
	sd	a5,-40(s0)
.L22:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L20
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L21
.L20:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L21:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L22
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a5,0(a5)
	bne	a4,a5,.L23
	sw	zero,-52(s0)
	j	.L24
.L26:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bne	a4,a5,.L25
	ld	a5,-72(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a4,8(a4)
	sd	a4,8(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	j	.L19
.L25:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L24:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L26
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-64(s0)
	sw	zero,-56(s0)
	sw	zero,-52(s0)
	ld	a5,-64(s0)
	sd	a5,-48(s0)
	j	.L27
.L30:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bleu	a4,a5,.L28
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a4,a5
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
	j	.L29
.L28:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a4,-1
	srli	a4,a4,32
	sd	a4,0(a5)
	li	a5,1
	sw	a5,-56(s0)
.L29:
	ld	a5,-48(s0)
	addi	a5,a5,16
	sd	a5,-48(s0)
.L27:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L30
	lw	a5,-56(s0)
	sext.w	a5,a5
	bne	a5,zero,.L31
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
.L31:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-64(s0)
	sd	a4,8(a5)
	ld	a5,-40(s0)
	j	.L19
.L23:
	li	a5,1
	sw	a5,-52(s0)
	j	.L32
.L34:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L32:
	lw	a5,-52(s0)
	sext.w	a4,a5
	li	a5,31
	bgt	a4,a5,.L33
	ld	a5,-72(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	s1,a0
	ld	a5,-40(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	s1,a5,.L34
.L33:
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L35
	ld	a5,-80(s0)
	ld	a5,32(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,32(a5)
	j	.L36
.L35:
	ld	a5,-80(s0)
	ld	a5,24(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,24(a5)
.L36:
	ld	a5,-72(s0)
.L19:
	mv	a0,a5
	ld	ra,72(sp)
	ld	s0,64(sp)
	ld	s1,56(sp)
	addi	sp,sp,80
	jr	ra
	.size	pat_insert, .-pat_insert
	.align	1
	.globl	pat_remove
	.type	pat_remove, @function
pat_remove:
	addi	sp,sp,-96
	sd	ra,88(sp)
	sd	s0,80(sp)
	addi	s0,sp,96
	sd	a0,-88(s0)
	sd	a1,-96(s0)
	ld	a5,-88(s0)
	beq	a5,zero,.L38
	ld	a5,-88(s0)
	ld	a5,8(a5)
	beq	a5,zero,.L38
	ld	a5,-40(s0)
	bne	a5,zero,.L39
.L38:
	li	a5,0
	j	.L40
.L39:
	ld	a5,-96(s0)
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
.L43:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L41
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L42
.L41:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L42:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L43
	ld	a5,-40(s0)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,0(a5)
	beq	a4,a5,.L44
	li	a5,0
	j	.L40
.L44:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	mv	a4,a5
	li	a5,1
	bne	a4,a5,.L45
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	bne	a5,zero,.L46
	li	a5,0
	j	.L40
.L46:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	beq	a4,a5,.L47
	li	a5,0
	j	.L40
.L47:
	ld	a5,-24(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
.L50:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L48
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L49
.L48:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L49:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L50
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L51
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,32(a5)
	j	.L52
.L51:
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,24(a5)
.L52:
	ld	a5,-64(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L53
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L54
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L55
.L54:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L55:
	ld	a4,-64(s0)
	sd	a5,32(a4)
	j	.L56
.L53:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L57
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L58
.L57:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L58:
	ld	a4,-64(s0)
	sd	a5,24(a4)
.L56:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	beq	a5,zero,.L59
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
.L59:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a4,-40(s0)
	ld	a5,-24(s0)
	beq	a4,a5,.L60
	ld	a5,-24(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	sd	a4,0(a5)
	ld	a5,-24(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	sd	a4,8(a5)
	ld	a5,-24(s0)
	lbu	a4,16(a5)
	ld	a5,-40(s0)
	sb	a4,16(a5)
.L60:
	ld	a0,-24(s0)
	call	free
	li	a5,1
	j	.L40
.L45:
	sw	zero,-52(s0)
	j	.L61
.L64:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L69
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L61:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L64
	j	.L63
.L69:
	nop
.L63:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L65
	li	a5,0
	j	.L40
.L65:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-72(s0)
	sw	zero,-52(s0)
	ld	a5,-72(s0)
	sd	a5,-48(s0)
	j	.L66
.L68:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L67
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a3,a4,a5
	ld	a5,-48(s0)
	addi	a4,a5,16
	sd	a4,-48(s0)
	li	a2,16
	mv	a1,a3
	mv	a0,a5
	call	memmove
.L67:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L66:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L68
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,-1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-72(s0)
	sd	a4,8(a5)
	li	a5,1
.L40:
	mv	a0,a5
	ld	ra,88(sp)
	ld	s0,80(sp)
	addi	sp,sp,96
	jr	ra
	.size	pat_remove, .-pat_remove
	.align	1
	.globl	pat_search
	.type	pat_search, @function
pat_search:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	sd	a1,-64(s0)
	sd	zero,-24(s0)
	ld	a5,-64(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	bne	a5,zero,.L71
	li	a5,0
	j	.L72
.L71:
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L73
	ld	a5,-32(s0)
	sd	a5,-24(s0)
.L73:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-36(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	ld	a1,-56(s0)
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L74
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L75
.L74:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L75:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	blt	a5,a4,.L71
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L76
	ld	a5,-32(s0)
	j	.L72
.L76:
	ld	a5,-24(s0)
.L72:
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	addi	sp,sp,64
	jr	ra
	.size	pat_search, .-pat_search
	.ident	"GCC:, (GNU), 9.2.0"
